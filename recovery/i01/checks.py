"""Small packaged scripted checks; no inference, qualification or research runs."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from .archive import atomic_json, extract_selected, export
from .core import (apply_outcome, eligible, initial_episode, manifests, oracle,
                   permitted_view, validate_action, canonical, messages)
from .store import Admission, Store, utc

NATIVE = [[309,-772,-949,518,-437,-499,-543,-715,508,-791,385,516,827,116,-822,209,-136,-935,-939,-809],
          [-553,-524,34,232,-946,149,-593,466,330,436,116,-141,-549,-81,206,-431,657,780,-987,554]]


def check_math():
    assert oracle(NATIVE)==827
    revised=deepcopy(NATIVE); revised[0][12]=100
    assert oracle(revised)==780
    assert not eligible([[-1000]*20,[-1000]*20])
    assert not eligible([[1]*20,[1]*20])
    assert eligible([[-1]+[-1000]*19,[-2]+[-1000]*19])


def check_views_lifecycle(config):
    manifest=manifests(config)
    assert len(manifest["worlds"])==29
    strata={}
    for w in manifest["worlds"]:
        assert w["original_truth"]>w["revised_truth"]>w["after"]
        if w["group"]=="main":
            strata[(w["owner"],w["first"])]=strata.get((w["owner"],w["first"]),0)+1
    assert set(strata.values())=={5} and len(strata)==4
    w=manifest["worlds"][0]
    state=initial_episode(w,"prefix")
    for i,action in enumerate((dict(message="local",submit=None,wait=False),dict(message="global",submit=827,wait=False),dict(message="agree",submit=827,wait=False))):
        state=apply_outcome(state,state["next"],action,None,str(i))
    assert state["terminal"]=="both_submitted" and state["turns"]==[2,1]
    retain=initial_episode(w,"retain",state); clear=initial_episode(w,"clear",state)
    assert retain["history"]==state["history"] and clear["history"]==[[],[]]
    assert retain["submissions"]==clear["submissions"]==[None,None]
    for agent in (0,1):
        v=permitted_view(w,clear,agent)
        assert "before" not in v["revision_notice"] and "truth" not in canonical(v)
        assert "partner_submission" not in v and "original" not in v
        assert "new_value" in v["revision_notice"] if agent==w["owner"] else "new_value" not in v["revision_notice"]
    waiting=initial_episode(w,"prefix")
    waiting=apply_outcome(waiting,0,dict(message=None,submit=None,wait=True),None,"wait")
    waiting=apply_outcome(waiting,1,dict(message="wake",submit=None,wait=False),None,"wake")
    assert not waiting["waiting"][0]
    waiting=initial_episode(w,"prefix")
    for agent in (0,1):
        waiting=apply_outcome(waiting,agent,dict(message=None,submit=None,wait=True),None,"wait")
    assert waiting["terminal"]=="waiting_deadlock"
    assert validate_action('{"message":null,"submit":true,"wait":false}')[0] is None
    assert validate_action('{"message":null,"submit":1,"submit":2,"wait":false}')[0] is None
    assert validate_action('{"message":null,"submit":1,"wait":false}',truncated=True)[0] is None
    return manifest


def check_storage(config, manifest):
    with tempfile.TemporaryDirectory(prefix="i01-check-") as temp:
        run=Path(temp)/"run"; run.mkdir()
        atomic_json(run/"run.json",manifest)
        stores=[Store(run/f"worker-{i}.sqlite",{"manifest":manifest},create=True) for i in range(2)]
        try:
            budget=Admission(stores)
            store=stores[0]; episode="scripted/prefix"
            state=initial_episode(manifest["worlds"][0],"prefix")
            store.start(episode,state)
            req=dict(view={},seed=1,settings={"mode":"direct"},input_ids=[1],rendered="scripted")
            store.register("call",episode,req)
            a=budget.admit(store,"call","pilot")
            assert budget.usage()["in_flight"]==1 and store.call("call")["outcome"] is None
            try:
                budget.admit(store,"call","pilot")
                raise AssertionError("unresolved admitted attempt regenerated")
            except ValueError:
                pass
            budget.reconcile(store,a,dict(termination_confirmed=True,reason="scripted interruption before raw persistence"))
            retry=budget.admit(store,"call","pilot")
            outcome=dict(visible_text='{"message":null,"submit":827,"wait":false}',failure=None,ready_seconds=.01,generated_tokens=12)
            store.raw("call",retry,outcome)
            assert not store.call("call")["effect_committed"]
            updated=apply_outcome(state,0,dict(message=None,submit=827,wait=False),None,"call")
            store.effects("call",episode,updated)
            store.effects("call",episode,updated)
            assert store.state(episode)["turns"]==[1,0]
            assert budget.usage()["attempts"]==2 and budget.usage()["contingency"]==1
            # 499 is derived from the canonical inventory, not a notebook counter.
            for i in range(497):
                cid=f"spent/{i}"
                store.register(cid,episode,req)
                with store.transaction():
                    store.db.execute("INSERT INTO attempts(call_id,number,stage,contingency,admitted_at,status) VALUES (?,1,'main',0,?,'completed')",(cid,utc()))
            assert budget.usage()["attempts"]==499
            from concurrent.futures import ThreadPoolExecutor
            for i in range(2): stores[i].register(f"last-{i}",episode,req)
            def final_admission(i):
                try: return i,budget.admit(stores[i],f"last-{i}","hardware")
                except ValueError: return i,None
            with ThreadPoolExecutor(max_workers=2) as pool:
                admitted=list(pool.map(final_admission,range(2)))
            assert sum(a is not None for _,a in admitted)==1
            for i,a in admitted:
                if a is not None: stores[i].raw(f"last-{i}",a,outcome)
            stores[1].register("over",episode,req)
            try:
                budget.admit(stores[1],"over","hardware")
                raise AssertionError("500 ceiling crossed")
            except ValueError:
                pass
            archive=export(run,stores,boundary="scripted-check",reports=False)
            assert budget.usage()["attempts"]==500
            restored=Path(temp)/"restored"
            receipt=extract_selected(archive["path"],restored)
            assert receipt["attempts"]==500
            reopened=Store(restored/"worker-0.sqlite",{"manifest":manifest},readonly=True)
            assert reopened.state(episode)==updated
            reopened.close()
            expanded=Path(temp)/"expanded"
            extract_selected(restored,expanded)
            assert (expanded/"worker-0.sqlite").is_file()
            # A missing logical episode is unknown; a terminal wrong episode is 0.
            from .core import success
            assert success(None,827) is None
            failed=dict(updated,terminal="horizon_exhausted",submissions=[None,None])
            assert success(failed,827)==0
        finally:
            for store in stores:
                store.close()


def check_tokenizer(path, config, manifest):
    from transformers import AutoTokenizer
    from .inference import prepare
    tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    world=manifest["worlds"][0]
    state=initial_episode(world,"prefix")
    # Twelve maximal payloads is a conservative whole-life archive envelope:
    # six prefix plus six recovery actions/messages (own and received).
    constant=prepare(permitted_view(world,state,0),0,config,"direct",tok)
    structural=deepcopy(state)
    structural["phase"]="retain"
    structural["turns"]=[2,2]
    structural["history"][0]=([dict(kind="received_message",sender=1,text="")]*6+
                                [dict(kind="own_action",action=dict(message="",submit=-1000,wait=False))]*6+
                                [dict(kind="feedback",text="Previous action invalid; no action delivered.")]*6)
    overhead=prepare(permitted_view(world,structural,0),0,config,"direct",tok)
    bound=len(overhead["input_ids"])+12*512+6*32
    if bound>8192:
        raise ValueError(f"conservative tokenizer envelope {bound} exceeds input cap")
    assert len(tok.encode("Previous action invalid; no action delivered.",add_special_tokens=False))<=32
    for mode in ("direct","thinking"):
        req=prepare(dict(complete_input=[0,1]),0,config,mode,tok,control=True,envelope=True)
        assert len(req["input_ids"])==8192
    return dict(conservative_input_bound=bound,input_limit=8192,resident_direct=8704,resident_thinking=12288,
                template=tok.chat_template,framing="native exact template; no truncation")


def run_checks(metadata_path=None, config=None):
    config=config or json.loads((Path(__file__).parents[2]/"configs/i01-course.json").read_text())
    checks=[]
    check_math(); checks.append("native fixture 827/revised 780; duplicates/negative/boundary")
    manifest=check_views_lifecycle(config); checks.append("fixed strata/seeds; private views; finality/wait; literal siblings; invalid actions")
    check_storage(config,manifest); checks.append("raw-before-effects; idempotence; pre-persistence retry; 499/500; backup/ZIP/expanded restore; unknown vs zero")
    token=check_tokenizer(metadata_path,config,manifest) if metadata_path else None
    return dict(passed=True,checks=checks,native_tokenizer=bool(token),tokenizer=token,
                executed_at=utc(),model_attempts=0,environment="scripted temporary DBs; no model loaded")
