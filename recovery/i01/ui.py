"""Thin notebook operator surface; all scientific logic is in the library."""

from html import escape
import json
from pathlib import Path
import shutil
import subprocess
import threading

from .archive import atomic_json, digest, extract_selected
from .client import Client
from .core import canonical
from .setup import host_inventory, install


class Operator:
    def __init__(self, source, scratch="/kaggle/temp/i01", working="/kaggle/working", run="/kaggle/working/i01-study"):
        self.source,self.scratch,self.working,self.run=map(Path,(source,scratch,working,run))
        self.client=None; self.environment=None; self.metadata=None; self.weights=None
        self.busy=threading.Lock(); self.outputs=[]
        self.deadline=None; self.allowance_evidence=None
        self.host=host_inventory(self.scratch,self.working)
        for name in ("environment","metadata","weights"):
            path=self.working/"i01-setup"/(name+".json")
            if path.exists(): setattr(self,name,json.loads(path.read_text()))

    def emit(self, event):
        # Scientific state remains in SQLite; this is only a live view.
        kind=event.get("kind")
        if kind=="admitted":
            line=f"{event['call']} · GPU slot {event['slot']} · attempt {event['attempt']} · {event['usage']['attempts']}/500"
        elif kind=="effect_committed":
            line=f"{event['world']} / {event['phase']} / agent {event['agent']}: {event['action'] or event['error']} · {event['terminal'] or 'continuing'}"
        elif kind=="checkpoint":
            line=f"Checkpoint {event['boundary']}: {event['bytes']:,} bytes; integrity {event['integrity']}"
        elif kind=="raw_persisted":
            o=event["outcome"]; line=f"Raw saved: {event['call']} · {o.get('generated_tokens')} tokens · {o.get('ready_seconds')} ready-model seconds"
        else:
            line=canonical(event)
        print(line,flush=True)

    def bootstrap_status(self):
        from IPython.display import display, HTML
        display(HTML('<h3>I-01 workspace inventory</h3><pre>'+escape(json.dumps(dict(host=self.host,source=str(self.source),run=str(self.run)),indent=2))+'</pre>'))

    def setup(self):
        self.environment=install(self.source,self.scratch,self.working)
        result=self._transport("metadata")
        self.metadata=result
        return self.environment

    def _transport(self, command):
        if self.environment is None:
            raise ValueError("complete Online setup first")
        from .setup import invoke
        log=self.working/"i01-setup"/(command+"-command.log")
        invoke([self.environment["interpreter"],"-m","recovery.i01.cli","--source",self.source,command,
                "--scratch",self.scratch,"--working",self.working],log,3600,
               env=self._env())
        return json.loads((self.working/"i01-setup"/(command+".json")).read_text())

    def _env(self):
        import os
        return dict(os.environ,HF_HUB_CACHE=str(self.scratch/"hf-cache"),HF_HUB_ETAG_TIMEOUT="30",HF_HUB_DOWNLOAD_TIMEOUT="60")

    def initialize(self, mode="new", selected=None, tail=None, evidence=""):
        if self.environment is None:
            raise ValueError("Online setup prerequisite missing")
        if mode not in ("new","restore","reopen"):
            raise ValueError("choose new, restore or reopen explicitly")
        if mode=="restore":
            if not selected or tail not in ("latest","unknown") or not evidence.strip():
                raise ValueError("select exact bundle and document latest-snapshot or unknown-tail evidence")
            extract_selected(selected,self.run)
        elif mode=="new":
            from .workflow import initialize
            config=json.loads((self.source/"configs/i01-course.json").read_text())
            initialize(self.run,self.source,config)
        elif not (self.run/"run.json").exists():
            raise ValueError("reopen requires files intact; no implicit new study")
        if self.client is not None and self.client.process.poll() is None:
            return self.client.command("status")
        self.client=Client(self.environment["interpreter"],self.source,self.run,self.scratch/"hf-cache",self.emit)
        self.receipt_session=self.client.command("status")["session"]
        if (self.working/"i01-setup").exists():
            shutil.copytree(self.working/"i01-setup",self.run/"receipts/setup"/self.receipt_session,dirs_exist_ok=True)
        if mode=="restore":
            self.client.command("lost_spending",gap=dict(resolved=tail=="latest",upper=0 if tail=="latest" else None,evidence=evidence))
        # Deadlines belong to this controller session; never reuse an old one.
        if self.deadline and self.allowance_evidence:
            self.client.action("window",deadline=self.deadline,evidence=self.allowance_evidence)
        return self.client.command("status")

    def set_window(self, deadline, evidence):
        self.deadline,self.allowance_evidence=deadline,evidence
        if self.client:
            return self.client.action("window",deadline=deadline,evidence=evidence)
        return dict(deadline=deadline,evidence=evidence,apply_after_initialization=True)

    def run_action(self, action, **args):
        if action=="setup": return self.setup()
        if action=="initialize": return self.initialize(**args)
        if action=="weights":
            if self.client is None: raise ValueError("initialize and self-check first")
            if not self.client.command("status")["gates"].get("selfcheck"):
                raise ValueError("native self-check prerequisite missing")
            self.weights=self._transport("weights")
            shutil.copytree(self.working/"i01-setup",self.run/"receipts/setup"/self.receipt_session,dirs_exist_ok=True)
            return self.weights
        if action=="window": return self.set_window(**args)
        if self.client is None:
            raise ValueError("initialize/restore/reopen the study first")
        if action=="selfcheck":
            if self.metadata is None: raise ValueError("metadata missing")
            args=dict(metadata_path=self.metadata["snapshot"])
        if action=="load":
            if self.weights is None: raise ValueError("verify/download weights first")
            args=dict(snapshot=self.weights["snapshot"],host=host_inventory(self.scratch,self.working))
        if action in ("status","pause","close_models"):
            return self.client.command(action)
        if action=="shutdown":
            self.client.close(); self.client=None
            return dict(processes_closed=True,provider_release="Stop Kaggle through its UI; process exit alone does not prove deallocation.")
        return self.client.action(action,**args)

    def verify_checkpoint(self):
        from .archive import verify
        from .report import analysis
        import tempfile
        selected=self.run/"exports/latest.zip"
        with tempfile.TemporaryDirectory(prefix="i01-reopen-",dir=self.working) as name:
            restored=Path(name)/"snapshot"
            receipt=extract_selected(selected,restored)
            rebuilt=analysis(restored)
            archived=json.loads((restored/"reports/analysis.json").read_text())
            if canonical(rebuilt)!=canonical(archived):
                raise ValueError("read-only reconstruction differs from archived reports")
        result=dict(integrity="passed",attempts=receipt["attempts"],boundary=receipt["boundary"],
                    reconstruction="exact outcomes/costs/traces/gates match archived analysis",model_attempts=0)
        self.show(result); return result

    # Explicit notebook commands are the fallback when widgets are unavailable.
    def run(self, action, **args):
        if action in ("pause","status"):
            result=self.run_action(action,**args)
            self.show(result); return result
        if not self.busy.acquire(blocking=False):
            raise ValueError("one active notebook action; use ui.run('pause') or status")
        try:
            result=self.run_action(action,**args)
            self.show(result)
            return result
        finally:
            self.busy.release()
            if (self.run/"exports/latest.zip").exists(): self.links()

    def show(self, result):
        from IPython.display import display, HTML
        display(HTML('<pre style="max-height:500px;overflow:auto;white-space:pre-wrap">'+escape(json.dumps(result,indent=2,default=str))+'</pre>'))

    def links(self):
        from IPython.display import display, HTML, FileLink
        zip_path=self.run/"exports/latest.zip"
        def link(path):
            try: target=path.relative_to(Path.cwd())
            except ValueError: target=path
            display(FileLink(str(target)))
        if zip_path.exists():
            import zipfile
            with zipfile.ZipFile(zip_path) as z:
                integrity=json.loads(z.read("integrity.json"))
            display(HTML(f'<p><b>Download the latest checkpoint off session.</b> {zip_path.stat().st_size:,} bytes · boundary {escape(integrity["boundary"])} · {escape(integrity["created_at"])} · SHA256 {digest(zip_path)}. A link does not prove a browser download succeeded.</p>'))
            link(zip_path)
            display(HTML('<p>If the frontend does not open this link, use Kaggle’s Output/Files pane to download this exact path. Save it outside the session.</p>'))
            display(HTML('<details><summary>Archive contents / integrity inventory</summary><pre>'+escape(json.dumps(integrity,indent=2))+'</pre></details>'))
        for relative in ("overview.html","overview.md","conversations.html","conversations.txt","conversations.jsonl","worlds.csv","paired-results.csv","costs.csv","attempts.csv","analysis.json"):
            p=self.run/"reports"/relative
            if p.exists(): link(p)
        for p in sorted((self.run/"reports/figures").glob("*")):
            if p.is_file(): link(p)

    def inspect(self, world=None, phase=None, agent=None):
        from .report import analysis
        from IPython.display import display, HTML
        if not (self.run/"run.json").exists():
            raise ValueError("initialize or restore first")
        result=analysis(self.run)
        self.show(result["summary"])
        display(HTML('<p>All complete prompts, private audit outputs and tokens remain in the conversation files. The selector below changes only this view.</p>'))
        for t in result["traces"]:
            req=json.loads(t["request"])
            if world and not t["episode"].startswith(world+"/"): continue
            if phase and t["episode"].split("/")[-1]!=phase: continue
            if agent is not None and req["view"].get("agent")!=agent: continue
            o=json.loads(t["outcome"]) if t["outcome"] else None
            display(HTML('<details><summary>'+escape(t["id"])+'</summary><h4>Exact permitted prompt</h4><pre style="white-space:pre-wrap">'+escape(req.get("rendered",""))+'</pre><h4>Evaluator audit: raw output, thinking, private submission and measurements</h4><pre style="white-space:pre-wrap">'+escape(json.dumps(o,indent=2))+'</pre></details>'))
        self.links()

    def annotate(self, identity, label, calls, notes):
        if self.client is None: raise ValueError("open controller for canonical annotation writes")
        return self.client.command("annotate",annotation=dict(id=identity,label=label,calls=calls,notes=notes))

    def panel(self, action, title=None, ceiling=0, **defaults):
        from IPython.display import display, HTML
        title=title or action
        description=(f'First-attempt ceiling: {ceiling}. Eligible identical infrastructure retries consume the shared 28 contingency and 500 whole-study ceiling.' if ceiling else 'Zero model generations; setup, state or reporting only.')
        display(HTML(f'<h3>{escape(title)}</h3><p>{description} Successful completion starts no later stage.</p>'))
        print(f"Explicit command: ui.run({action!r}"+"".join(f", {k}={v!r}" for k,v in defaults.items())+")")
        try:
            import ipywidgets as widgets
        except ImportError:
            print("Widgets unavailable. Use the explicit finite command printed above."); return
        fields={}
        if action=="review" and defaults.get("scope")=="" and self.client:
            batch=self.client.command("status")["gates"].get("batch",{})
            defaults["scope"]=batch.get("id","")
        labels=dict(mode="Mode",selected="Restore path",tail="Snapshot tail",evidence="Evidence",
                    deadline="UTC deadline",notes="Review notes",reason="Competence reason",scope="Review scope",
                    useful_communication="Useful original communication",usable="Pilot usable",reload="Reload probes")
        for key,value in defaults.items():
            if key=="mode" and action=="initialize": fields[key]=widgets.Dropdown(options=["new","restore","reopen"],value=value,description=key)
            elif key=="mode" and action in ("screen","envelope"): fields[key]=widgets.Dropdown(options=["direct","thinking"],value=value,description=key)
            elif key=="tail": fields[key]=widgets.Dropdown(options=["latest","unknown"],value=value,description=key)
            elif type(value) is bool: fields[key]=widgets.Checkbox(value=value,description=key)
            elif type(value) is int: fields[key]=widgets.IntText(value=value,description=key)
            else: fields[key]=widgets.Text(value="" if value is None else str(value),description=key,layout=widgets.Layout(width="95%"))
            if key in ("notes","reason","evidence"):
                fields[key]=widgets.Textarea(value="" if value is None else str(value),description=key,layout=widgets.Layout(width="95%"))
            fields[key].description=labels.get(key,key)
            fields[key].style.description_width="initial"
        button=widgets.Button(description=title,button_style="primary",layout=widgets.Layout(width="auto"))
        if action=="screen":
            fields["mode"].disabled=True
            if defaults.get("mode")=="thinking":
                direct=(self.client.command("status")["gates"].get("screen/direct",{}) if self.client else {})
                allowed=bool(direct and not direct.get("passed") and not direct.get("protocol_errors"))
                def thinking_enabled(change=None):
                    button.disabled=not (allowed and fields.get("reason") and fields["reason"].value.strip())
                if "reason" in fields: fields["reason"].observe(thinking_enabled,names="value")
                thinking_enabled()
        output=widgets.Output(); self.outputs.append(output)
        def clicked(_):
            if self.busy.locked() and action not in ("pause","status"):
                with output: print("An action is active; pause or inspect status.")
                return
            def work():
                with output:
                    try: self.run(action,**{k:v.value for k,v in fields.items()})
                    except Exception as error: print(f"Stopped: {error}")
            threading.Thread(target=work,daemon=True).start()
        button.on_click(clicked)
        display(widgets.VBox([*fields.values(),button,output]))
        display(HTML('<p>Run this cell to render controls. Generation begins only after the button or explicit command. If the frontend does not render the control reliably, use the printed command; do not enable automatic progression.</p>'))

    def inspect_panel(self, default_world=None):
        from IPython.display import display
        try:
            import ipywidgets as widgets
        except ImportError:
            print(f"Explicit inspection: ui.inspect(world={default_world!r})"); self.links(); return
        worlds=[("All worlds","")]
        if (self.run/"run.json").exists():
            worlds += [(w["id"],w["id"]) for w in json.loads((self.run/"run.json").read_text())["worlds"]]
        world=widgets.Dropdown(options=worlds,value=default_world if default_world in [v for _,v in worlds] else "",description="World")
        phase=widgets.Dropdown(options=[("All phases",""),("Prefix","prefix"),("Retain","retain"),("Clear","clear")],description="Phase")
        agent=widgets.Dropdown(options=[("All agents",None),("Agent 0",0),("Agent 1",1)],description="Agent")
        button=widgets.Button(description="Inspect complete trace")
        output=widgets.Output()
        def inspect(_):
            with output:
                output.clear_output(wait=True)
                try: self.inspect(world.value or None,phase.value or None,agent.value)
                except Exception as error: print(error)
        button.on_click(inspect)
        display(widgets.VBox([widgets.HBox([world,phase,agent]),button,output])); self.links()
