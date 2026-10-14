"""Thin notebook operator surface; all scientific logic is in the library."""

from html import escape
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import threading

from .archive import atomic_json, digest, extract_selected
from .client import Client
from .core import canonical
from .setup import host_inventory, install


class ActionStopped(ValueError):
    """A finite action stopped; its durable evidence remains inspectable."""


def _display(body, plain):
    try:
        from IPython import get_ipython
        from IPython.display import display, HTML
        if get_ipython() is None: print(plain, flush=True)
        else: display(HTML(body))
    except ImportError:
        print(plain, flush=True)


def _text(value):
    if value is None: return "Unknown / not recorded"
    if type(value) is bool: return "Yes" if value else "No"
    return str(value)


def _table(headers, rows, title=None):
    rows=list(rows)
    body=(f'<h3>{escape(title)}</h3>' if title else '')
    body+='<table style="border-collapse:collapse;width:100%;text-align:left"><thead><tr>'
    body+=''.join('<th style="padding:.5em;border-bottom:1px solid #888">'+escape(h)+'</th>' for h in headers)
    body+='</tr></thead><tbody>'
    body+=''.join('<tr>'+''.join('<td style="padding:.5em;border-bottom:1px solid #8884;vertical-align:top;overflow-wrap:anywhere">'+escape(_text(v))+'</td>' for v in row)+'</tr>' for row in rows)
    body+='</tbody></table>'
    _display(body, ('\n'+title+'\n' if title else '')+' | '.join(headers)+'\n'+'\n'.join(' | '.join(_text(v) for v in row) for row in rows))


def _details(title, value):
    text=value if isinstance(value,str) else json.dumps(value,indent=2,default=str,ensure_ascii=False)
    _display('<details><summary>'+escape(title)+'</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere">'+escape(text)+'</pre></details>',title+'\n'+text)


class Operator:
    def __init__(self, source, scratch="/kaggle/temp/i01", working="/kaggle/working", run="/kaggle/working/i01-study"):
        self.source,self.scratch,self.working,self.run_dir=map(Path,(source,scratch,working,run))
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
        elif kind=="worker_progress":
            line=f"Working · {event.get('elapsed_seconds')}s · {event.get('text')}"
        elif kind=="action_finished":
            line=f"{event['action']}: {event.get('error') or 'complete'} · checkpoint {event.get('checkpoint',{}).get('path','unavailable')}"
        elif kind=="action_stopped":
            line=f"Stopped {event['action']}: {event['error']}"
        else:
            line=f"{kind or 'Progress'}: "+str(event.get('text',event.get('error','recorded in the stage receipt')))
        print(line,flush=True)

    def bootstrap_status(self):
        _table(['Workspace','Observed value'], [('Python',self.host['python']),('System',self.host['system']),
               ('Source',self.source),('Study files',self.run_dir)], 'Workspace')
        _table(['Device','Model','UUID','Memory (MiB)'],[(g['index'],g['name'],g['uuid'],g['memory_mib']) for g in self.host['gpus']], 'Actual GPU inventory')
        _table(['Storage','Path','Free GiB'],[(k,v['path'],round(v['free']/2**30,2)) for k,v in self.host['paths'].items()])
        if self.host.get('gpus_error'): print('GPU inventory unavailable: '+self.host['gpus_error'])
        print('Next: run Install the pinned runtime. Host acceptance still occurs before installation.')

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
            extract_selected(selected,self.run_dir)
        elif mode=="new":
            from .workflow import initialize
            config=json.loads((self.source/"configs/i01-course.json").read_text())
            initialize(self.run_dir,self.source,config)
        elif not (self.run_dir/"run.json").exists():
            raise ValueError("reopen requires files intact; no implicit new study")
        if self.client is not None and self.client.process.poll() is None:
            return self.client.command("status")
        self.client=Client(self.environment["interpreter"],self.source,self.run_dir,self.scratch/"hf-cache",self.emit)
        self.receipt_session=self.client.command("status")["session"]
        if (self.working/"i01-setup").exists():
            shutil.copytree(self.working/"i01-setup",self.run_dir/"receipts/setup"/self.receipt_session,dirs_exist_ok=True)
        if mode=="restore":
            self.client.command("lost_spending",gap=dict(resolved=tail=="latest",upper=0 if tail=="latest" else None,evidence=evidence))
        # Deadlines belong to this controller session; never reuse an old one.
        if self.deadline and self.allowance_evidence:
            receipt=self.client.action("window",deadline=self.deadline,evidence=self.allowance_evidence)
            if receipt.get('error') or receipt.get('checkpoint',{}).get('error'):
                self.show(receipt)
                raise ActionStopped(receipt.get('error') or receipt['checkpoint']['error'])
        return self.client.command("status")

    def set_window(self, deadline, evidence):
        if not isinstance(deadline,str) or not isinstance(evidence,str) or not evidence.strip():
            raise ValueError('Set the actual UTC session deadline and allowance evidence in the configuration cell.')
        value=datetime.fromisoformat(deadline)
        if value.tzinfo is None or value<=datetime.now(timezone.utc):
            raise ValueError('Session deadline must be an actual future time with a UTC offset.')
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
            shutil.copytree(self.working/"i01-setup",self.run_dir/"receipts/setup"/self.receipt_session,dirs_exist_ok=True)
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
        selected=self.run_dir/"exports/latest.zip"
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

    # Ordinary cells use this same finite path as legacy widget callbacks.
    def run(self, action, **args):
        self._last_action=action
        if action in ("pause","status"):
            result=self.run_action(action,**args)
            self.show(result); return result
        if not self.busy.acquire(blocking=False):
            raise ValueError("one active notebook action; request pause or inspect status before another stage")
        try:
            result=self.run_action(action,**args)
            self.show(result)
            if action in ('pilot','main') and (self.run_dir/'run.json').exists():
                worlds=[f"pilot-{args['number']-1:02d}"] if action=='pilot' else self.status()['gates'].get('batch',{}).get('worlds',[])
                self.inspect(worlds=worlds, downloads=False)
            error=result.get('error') if isinstance(result,dict) else None
            if isinstance(result,dict) and result.get('checkpoint',{}).get('error'):
                error=(error+'; ' if error else '')+'Checkpoint failed: '+result['checkpoint']['error']
            payload=result.get('result',result) if isinstance(result,dict) else result
            if isinstance(payload,dict) and payload.get('passed') is False and action in ('selfcheck','readiness','screen','envelope'):
                error=error or f'{action} gate did not pass. Inspect the recorded evidence; no later stage has started.'
            if action=='selfcheck' and isinstance(payload,dict) and not payload.get('native_tokenizer'):
                error=error or 'Native tokenizer acceptance is required; the scripted-only receipt does not qualify this host.'
            if error: raise ActionStopped(error)
            return result
        except KeyboardInterrupt:
            print("Pause requested. An admitted call may still be active. Inspect status; wait for settlement before snapshot/close. Rerun only the saved scope.")
            raise
        except ActionStopped:
            raise
        except Exception as error:
            if action in ('setup','weights'):
                print(f'Stopped {action}: {error}. Setup/download logs are in {self.working / "i01-setup"}.')
            else:
                print(f'Stopped {action}: {error}. Saved evidence remains available through study.inspect() and study.links().')
            raise
        finally:
            self.busy.release()
            if (self.run_dir/"exports/latest.zip").exists(): self.links()

    def show(self, result):
        action=getattr(self,'_last_action','Result')
        payload=result.get('result',result) if isinstance(result,dict) else result
        error=result.get('error') if isinstance(result,dict) else None
        _display(f'<h3>{escape(action.replace("_"," ").title())} — {"stopped" if error else "result"}</h3>',f'{action}: {error or "result"}')
        if error: _display('<p><strong>'+escape(error)+'</strong></p>',error)
        if isinstance(payload,dict):
            rows=[(k.replace('_',' ').capitalize(),v) for k,v in payload.items() if v is None or isinstance(v,(str,int,float,bool))]
            if rows: _table(['Measurement','Recorded value'],rows)
            if 'known_pairs' in payload:
                _table(['Main coverage','Value'],[('Known paired outcomes',f"{payload['known_pairs']} / 20"),
                    ('New physical attempts',f"{payload['attempts']} / 500"),('Clear minus retain',payload['clear_minus_retain']),
                    ('Unknown-outcome bounds',payload['missingness_bounds'])])
            if 'models' in payload:
                _table(['Logical slot','Resident','Load receipt'],[(i,m['resident'],'Recorded' if m.get('load_report') else 'Not recorded') for i,m in enumerate(payload['models'])])
            if action=='screen' and 'correct' in payload:
                print(f"Competence: {payload['correct']}/12 correct; {payload['protocol_errors']} protocol errors. Required: at least 11/12 and zero protocol errors.")
            if action=='readiness' and payload.get('results'):
                _table(['Slot','Probe','Raw visible reply','Finite score steps','Fresh cache'],[(r['slot'],r['label'],r['outcome'].get('visible_text'),r['outcome'].get('backend',{}).get('finite_score_steps'),r['outcome'].get('backend',{}).get('cache',{}).get('initial_empty')) for r in payload['results']])
            if action=='prepare_batch':
                _table(['Prepared scope','Value'],[('Worlds',', '.join(payload.get('worlds',[])) or 'No remaining worlds'),('First-attempt ceiling',payload.get('first_ceiling')),('Eligible retry allowance',payload.get('eligible_retry_allowance'))])
                if payload.get('forecast'):
                    _table(['Resource forecast','Value'],list(payload['forecast'].items()))
            if action=='selfcheck':
                _table(['Lightweight check','State'],[(name,'Passed') for name in payload.get('checks',[])])
                print('Native tokenizer: '+('passed' if payload.get('native_tokenizer') else 'not accepted on this host'))
            if 'usage' in payload:
                _table(['Budget','Value'],[(k.replace('_',' '),v) for k,v in payload['usage'].items()])
            if action=='envelope' and payload.get('results'):
                _table(['Slot','Generated tokens','Observed free headroom (GiB)','Failure'],[(i,o.get('generated_tokens'),round(o['backend']['observed_peak_free_lower_bytes']/2**30,3) if o.get('backend',{}).get('observed_peak_free_lower_bytes') is not None else None,o.get('failure') or 'None recorded') for i,o in enumerate(payload['results'])])
            # Full replies/tokens live in the trace files; avoid embedding them in
            # every hidden receipt DOM as well as the dedicated audit display.
            compact={k:v for k,v in payload.items() if k not in ('results','manifest','sessions','identity','versions','host')}
            if payload.get('results') is not None: compact['raw_result_count']=len(payload['results'])
            if 'gates' in compact: compact['gates']=list(compact['gates'])
            _details('Receipt summary; complete evidence is in the reports and checkpoint',compact)
        elif isinstance(payload,list):
            _table(['Logical slot','CUDA UUID','Load seconds','Total device GiB'],[(i,r.get('cuda_device_uuid'),r.get('load_seconds'),round(r['total_device_bytes']/2**30,2) if r.get('total_device_bytes') is not None else None) for i,r in enumerate(payload) if isinstance(r,dict)],'Resident load evidence')
            _details('Load receipts',payload)
        checkpoint=result.get('checkpoint',{}) if isinstance(result,dict) else {}
        if checkpoint: print('Checkpoint: '+str(checkpoint.get('error') or checkpoint.get('integrity','not recorded')))

    def status(self):
        if self.client is None: raise ValueError('Open or restore the study first.')
        return self.client.command('status')

    def open_study(self, mode='new', *, deadline=None, allowance_evidence='', selected=None, tail=None, evidence=''):
        receipt=self.set_window(deadline,allowance_evidence)
        if receipt.get('error') or receipt.get('checkpoint',{}).get('error'):
            self.show(receipt)
            raise ActionStopped(receipt.get('error') or receipt['checkpoint']['error'])
        return self.run('initialize',mode=mode,selected=selected,tail=tail,evidence=evidence)

    def selected_mode(self):
        gates=self.status()['gates']
        mode=gates.get('freeze',{}).get('mode') or gates.get('selected_mode')
        if mode: return mode
        for mode in ('direct','thinking'):
            if gates.get('screen/'+mode,{}).get('passed'): return mode
        raise ValueError('No passing competence screen. Inspect qualification before envelope or pilots.')

    def thinking_screen(self, reason=None):
        direct=self.status()['gates'].get('screen/direct',{})
        if direct.get('passed'):
            print('Direct mode passed. Thinking qualification is skipped; zero new attempts.')
            return dict(skipped=True)
        if not direct or direct.get('protocol_errors') or not isinstance(reason,str) or not reason.strip():
            raise ValueError('Thinking requires a recorded direct competence limitation without protocol errors and your explicit justification.')
        return self.run('screen',mode='thinking',reason=reason)

    def envelope(self, *, reload=False):
        return self.run('envelope',mode=self.selected_mode(),reload=reload)

    def review_pilot(self, number, *, useful_communication=None, usable=None, notes=''):
        if type(number) is not int or number not in (1,2,3): raise ValueError('Pilot number must be 1, 2 or 3.')
        if type(useful_communication) is not bool or type(usable) is not bool or not notes.strip():
            raise ValueError('Inspect this pilot, then supply actual communication/usability findings (True or False) and review notes. Unreviewed is not approved.')
        return self.run('review',scope=f'pilot-{number}',notes=notes,useful_communication=useful_communication,usable=usable)

    def run_batch(self):
        batch=self.status()['gates'].get('batch')
        if not batch: raise ValueError('Run Prepare the next main batch first.')
        if batch.get('complete'):
            print('The saved batch is complete; zero new calls. Inspect/acknowledge it before preparing another.')
            self.inspect(worlds=batch.get('worlds',[]))
            return batch
        return self.run('main')

    def review_batch(self, notes=''):
        batch=self.status()['gates'].get('batch')
        if not batch or not batch.get('complete'): raise ValueError('Run or resume the saved batch before acknowledging it.')
        if batch['id']=='main-complete':
            print('All main scopes are recorded. Next: build the final report.')
            return batch
        self.inspect(worlds=batch['worlds'],downloads=False)
        acknowledgement=f"Operator executed the review cell for saved scope {batch['id']}; understanding and browser download are not verified."
        return self.run('review',scope=batch['id'],notes=notes.strip() or acknowledgement)

    def preview_freeze(self):
        status=self.status()
        config=json.loads((self.run_dir/'run.json').read_text())['config']
        _table(['Gate','Recorded state'],[(k,'Passed' if status['gates'].get(k,{}).get('passed') else 'Not passed / not recorded') for k in ('readiness','screen/direct','screen/thinking','envelope')], 'Qualification')
        _table(['Pilot','Communication','Usable','Review notes'],[(i,status['gates'].get(f'review/pilot-{i}',{}).get('useful_communication'),status['gates'].get(f'review/pilot-{i}',{}).get('usable'),status['gates'].get(f'review/pilot-{i}',{}).get('notes')) for i in (1,2,3)], 'Pilot reviews')
        self.inspect(worlds=[f'pilot-{i:02d}' for i in range(3)],audit_limit=0,downloads=False)
        forecast=self.client.command('forecast')
        _table(['Resource forecast','Value'],list(forecast.items()),'Main admission forecast')
        _details('Exact configuration proposed for freeze',config)
        print('Review these saved findings/configuration. Next: run Freeze for main with your notes. This cell does not freeze or generate.')
        return forecast

    def links(self, all_files=False):
        from urllib.parse import quote
        zip_path=self.run_dir/"exports/latest.zip"
        def link(path,label=None):
            try: target=path.relative_to(Path.cwd())
            except ValueError: target=path
            return '<a href="'+escape(quote(target.as_posix(),safe='/'),quote=True)+'">'+escape(label or path.name)+'</a>'
        if zip_path.exists():
            import zipfile
            try:
                with zipfile.ZipFile(zip_path) as z: integrity=json.loads(z.read("integrity.json"))
                caption=f"{zip_path.stat().st_size:,} bytes · {integrity['boundary']} · {integrity['created_at']}"
                _display('<p><strong>'+link(zip_path,'Download latest cumulative checkpoint')+'</strong><br>'+escape(caption)+'</p>', 'Checkpoint: '+str(zip_path)+'\n'+caption)
                _details('Checkpoint SHA256 and integrity inventory',dict(sha256=digest(zip_path),**integrity))
            except (OSError,ValueError,KeyError,zipfile.BadZipFile) as error:
                print(f'Checkpoint inventory unavailable: {error}. Inspect {zip_path}; do not claim restore acceptance.')
            _display('<p>Save this ZIP outside Kaggle. It advances after later actions. If the link is unsupported, download <code>'+escape(str(zip_path))+'</code> from Output/Files. Link creation does not verify a download.</p>',f'Save outside Kaggle using Output/Files: {zip_path}; a link does not verify downloading.')
        report_dir=self.run_dir/'reports'
        relevant=[report_dir/n for n in ('overview.html','conversations.html','conversations.txt','worlds.csv') if (report_dir/n).is_file()]
        if relevant: _display('<p>'+' · '.join(link(p) for p in relevant)+'</p>','Reports: '+', '.join(str(p) for p in relevant))
        files=sorted(p for p in report_dir.rglob('*') if p.is_file())
        if files:
            inventory='<ul>'+''.join('<li>'+link(p,str(p.relative_to(report_dir)))+'</li>' for p in files)+'</ul>'
            _display(inventory if all_files else '<details><summary>All reports, tables, raw traces and figures</summary>'+inventory+'</details>', 'All report files:\n'+'\n'.join(str(p) for p in files))

    def inspect(self, world=None, phase=None, agent=None, *, worlds=None, audit_limit=6, downloads=True):
        from .report import analysis
        if not (self.run_dir/"run.json").exists():
            raise ValueError("initialize or restore first")
        if audit_limit is not None and (type(audit_limit) is not int or audit_limit<0): raise ValueError('audit_limit must be nonnegative or None for all calls.')
        result=analysis(self.run_dir)
        selected={world} if world else (set(worlds) if worlds is not None else None)
        rows=[r for r in result['worlds'] if selected is None or r['id'] in selected]
        gates=result['summary']['gates']
        mode=gates.get('selected_mode') or ('thinking' if gates.get('screen/thinking',{}).get('passed') else 'direct')
        def score(v): return 'Unknown / not executed' if v is None else ('Correct' if v else 'Unsuccessful (recorded)')
        if rows and all(r['group']=='qualification' for r in rows):
            _table(['World','Original control','Revised control'],[(r['id'],score(r.get('control_original_'+mode)),score(r.get('control_revised_'+mode))) for r in rows],mode.title()+' qualification controls')
        elif rows and all(r['group']=='main' for r in rows):
            _table(['World','Original team','Retain','Clear','Revised control'],[(r['id'],score(r['prefix']),score(r['retain']),score(r['clear']),score(r.get('control_revised_'+mode))) for r in rows], 'Recorded main outcomes')
        else:
            _table(['World','Original team','Retain','Clear','Original control','Revised control'],[(r['id'],score(r['prefix']),score(r['retain']),score(r['clear']),score(r.get('control_original_'+mode)),score(r.get('control_revised_'+mode))) for r in rows], 'Recorded outcomes')
        s=result['summary']
        print(f"Main paired coverage: {s['known_pairs']}/20 intended worlds. New physical attempts: {s['attempts']}/500; recorded contingency: {s['contingency']}/28. Historical 45 remain separate.")
        if self.client is not None:
            status=self.status(); usage=status.get('usage',{})
            if usage: _table(['Admission resource','Value'],[('Remaining attempt allowance',usage['remaining']),('Contingency including bounded lost spending',usage['contingency']),('Lost spending evidence',usage['lost_spending']),('Remaining session seconds',status['remaining_session_seconds'])])
        if not rows or not all(r['group']=='qualification' for r in rows):
            _table(['World','Phase','Calls','Generated tokens','Ready-model seconds','Messages'],[(r['world'],r['phase'],r['calls'],r['generated_tokens'],r['ready_seconds'],r['messages']) for r in result['costs'] if (selected is None or r['world'] in selected) and (not phase or r['phase']==phase)], 'Phase effort (unknown is not zero)')
        for ep in result['episodes']:
            identity,ep_phase=ep['id'].split('/',1)
            if selected is not None and identity not in selected: continue
            if phase and ep_phase!=phase: continue
            state=json.loads(ep['state'])
            # Events are already in their committed invocation/delivery order.
            _display('<h4>'+escape(ep['id'])+' · '+escape(str(state.get('terminal') or 'unfinished'))+'</h4>',ep['id']+' · '+str(state.get('terminal') or 'unfinished'))
            for event in state.get('events',[]):
                if agent is not None and event['agent']!=agent: continue
                act=event.get('action')
                prefix=f"Agent {event['agent']} · {event['call']}"
                if act and act.get('message') is not None:
                    _display('<p><strong>'+escape(prefix)+'</strong> → Agent '+str(1-event['agent'])+'</p><pre style="white-space:pre-wrap;overflow-wrap:anywhere">'+escape(act['message'])+'</pre>',prefix+' → Agent '+str(1-event['agent'])+'\n'+act['message'])
                elif act: print(prefix+(' · waiting' if act.get('wait') else ' · no public message'))
                else: print(prefix+' · invalid/failed action; no message delivered: '+str(event.get('error')))
            _details('Private evaluator audit: submissions, retained history and phase boundary',state)
        _details('Private evaluator audit: source edits and exact truth',[(w) for w in json.loads((self.run_dir/'run.json').read_text())['worlds'] if selected is None or w['id'] in selected])
        shown=0; matched=0
        for t in result["traces"]:
            req=json.loads(t["request"])
            if selected is not None and t['episode'].split('/')[0] not in selected: continue
            if phase and t["episode"].split("/")[-1]!=phase: continue
            if agent is not None and req["view"].get("agent")!=agent: continue
            matched+=1
            if audit_limit is not None and shown>=audit_limit: continue
            o=json.loads(t["outcome"]) if t["outcome"] else None
            _details('Exact permitted prompt and private raw audit: '+t['id'],dict(prompt=req.get('rendered',''),request=req,outcome=o,effect_committed=t['effect_committed']))
            shown+=1
        if matched>shown: print(f'Showing {shown}/{matched} detailed call audits. Complete prompts/replies/tokens remain in conversations.html/.txt/.jsonl. Use study.inspect(..., audit_limit=None) to display all calls.')
        if downloads: self.links()
        return result

    def final_report(self):
        if self.client is not None:
            receipt=self.run('report')
        else:
            from .report import write_report
            receipt=write_report(self.run_dir,self.run_dir/'reports')['summary']
            self.show(receipt); self.links()
        from .report import analysis
        result=analysis(self.run_dir)
        _table(['Paired outcome','Worlds'],list(result['summary']['paired_counts'].items()),'All twenty intended main worlds')
        try:
            from IPython.display import display, Image
            for path in sorted((self.run_dir/'reports/figures').glob('*.png')): display(Image(filename=str(path)))
        except ImportError: print('Figures available in the report files.')
        return receipt

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
        if (self.run_dir/"run.json").exists():
            worlds += [(w["id"],w["id"]) for w in json.loads((self.run_dir/"run.json").read_text())["worlds"]]
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
