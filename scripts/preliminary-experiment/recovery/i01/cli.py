"""Finite CLI and retained local JSON command loop for the I-01 notebook."""

import argparse
import json
import os
from pathlib import Path
import sys
import threading

from .archive import atomic_json, digest, extract_selected
from .core import canonical
from .store import restore_tail, resolve_restore_tail, charged_gap


def serve(run, source):
    # Initialize CPU plotting extensions on the controller's main thread before
    # entering blocking stdin I/O (Windows NumPy DLL initialization can deadlock
    # when its first import happens on an action thread).
    os.environ['MPLBACKEND']='Agg'
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot
    from .workflow import Session
    output_lock=threading.Lock()
    def send(value):
        with output_lock:
            print(canonical(value),flush=True)
    session=Session(run,source,progress=lambda e:send(dict(event=e)))
    active=None
    completed={}
    def execute(identity,action,args):
        result=session.run_action(action,**args)
        completed[identity]=result
        send(dict(done=identity,result=result))
    try:
        send(dict(ready=True,study=session.manifest["study_id"]))
        for line in sys.stdin:
            identity=None
            try:
                req=json.loads(line); identity=req["id"]; op=req["op"]
                busy=active is not None and active["thread"].is_alive()
                if op=="start":
                    if busy:
                        if active["action"]==req["action"] and active["args"]==req.get("args",{}):
                            value=dict(attached=active["id"])
                        else:
                            raise ValueError("one active action; pause or wait before another")
                    else:
                        session.meta.put_meta("operator_authorization",dict(action=req["action"],args=req.get("args",{}),evidence=req.get("authorization","Explicit finite CLI request")))
                        thread=threading.Thread(target=execute,args=(identity,req["action"],req.get("args",{})),daemon=True)
                        active=dict(id=identity,action=req["action"],args=req.get("args",{}),thread=thread)
                        thread.start(); value=dict(started=identity)
                elif op=="pause":
                    session.pause.set(); value=dict(pause_requested=True,quiescent=not busy)
                elif op=="status":
                    value=session.status()
                elif op=="forecast":
                    value=session.forecast()
                elif op=="result":
                    value=completed.get(req["action_id"],dict(pending=True))
                elif op=="close_models":
                    value=session.close_models()
                    session.checkpoint("close-models")
                elif op=='failure_cleanup':
                    if busy:
                        session.pause.set()
                        raise ValueError('Pause requested; wait for action settlement before cleanup')
                    from .policy import FAILURE_CLEANUP_POLICIES
                    if session.meta.meta('execution_plan',{}).get('policy') not in FAILURE_CLEANUP_POLICIES:
                        raise ValueError('Unattended cleanup requires an approved Run All plan')
                    value=session.failure_cleanup(req['action'],req['error'])
                elif op=="reconcile":
                    if busy: raise ValueError("pause before reconciliation")
                    # A stale PID alone is not termination evidence. Operator must
                    # confirm old controller/model exit before this command.
                    session.admission.reconcile(session.stores[req["slot"]],req["attempt"],req["evidence"])
                    value=dict(reconciled=True)
                elif op=="confirm_timeout_termination":
                    if busy: raise ValueError("pause before termination reconciliation")
                    store=session.stores[req["slot"]]
                    row=store.call(req["call"])
                    evidence=req["evidence"]
                    if not row or not row["outcome"] or json.loads(row["outcome"]).get("failure")!="timeout" or not evidence.get("termination_confirmed") or not evidence.get("reason"):
                        raise ValueError("recorded timeout and explicit confirmed-exit evidence required")
                    store.put_meta("timeout_termination/"+req["call"],evidence)
                    value=dict(termination_confirmed=True,retry_allowed=False)
                elif op=="lost_spending":
                    if busy: raise ValueError("pause before evidence-gap reconciliation")
                    gap=req["gap"]
                    if gap.get("resolved") and (type(gap.get("upper")) is not int or not 0<=gap["upper"]<=28 or not gap.get("evidence")):
                        raise ValueError("bounded missing attempts and evidence required; unknown is not zero")
                    affected=req.get("affected_worlds",[])
                    world_ids={w["id"] for w in session.manifest["worlds"]}
                    if gap.get("upper",0) and (not affected or any(w not in world_ids for w in affected)):
                        raise ValueError("nonzero lost spending needs exact affected world IDs; lost prefixes cannot regenerate")
                    old=session.meta.meta('lost_spending',{})
                    minimum=charged_gap(old)
                    if gap.get('resolved') and (gap['upper']<minimum or old.get('additional_tail')=='unknown'):
                        raise ValueError('Do not erase the saved gap; use resolve_restore_tail for an additional unknown tail')
                    session.meta.put_meta("lost_spending",gap)
                    session.meta.put_meta("blocked_worlds",sorted(set(session.meta.meta('blocked_worlds',[]))|set(affected)))
                    value=gap
                elif op=='restore_tail':
                    if busy: raise ValueError('Pause before tail reconciliation')
                    value=restore_tail(session.meta,req['tail'],req['evidence'],boundary=req['boundary'])
                elif op=='resolve_restore_tail':
                    if busy:raise ValueError('Pause before tail reconciliation')
                    affected=req.get('affected_worlds',[])
                    worlds={w['id'] for w in session.manifest['worlds']}
                    if any(w not in worlds for w in affected) or req['upper'] and not affected:
                        raise ValueError('Additional lost attempts require exact affected-world IDs')
                    value=resolve_restore_tail(session.meta,req['upper'],req['evidence'],affected)
                elif op=="annotate":
                    if busy: raise ValueError("pause before annotations")
                    ann=req["annotation"]
                    if ann["label"] not in session.config["rubric"] or not ann.get("notes") or not ann.get("calls"):
                        raise ValueError("frozen label, notes and exact call references required")
                    call_ids={r["id"] for s in session.stores for r in s.rows("calls")}
                    if any(c not in call_ids for c in ann["calls"]):
                        raise ValueError("annotation references unknown call")
                    with session.meta.transaction():
                        session.meta.db.execute("INSERT OR REPLACE INTO annotations VALUES (?,?)",(ann["id"],canonical(ann)))
                    value=ann
                elif op=="close":
                    if busy:
                        session.pause.set(); raise ValueError("pause requested; wait for safe boundary then close")
                    value=session.close_models()
                    session.checkpoint("controller-close")
                    send(dict(id=identity,result=value)); break
                else:
                    raise ValueError("unknown management operation")
                send(dict(id=identity,result=value))
            except Exception as error:
                send(dict(id=identity,error=f"{type(error).__name__}: {error}"))
    finally:
        session.pause.set()
        # EOF means notebook owner disappeared. Terminate children immediately;
        # admitted outcomes without persistence remain unresolved and spent.
        if active is not None and active["thread"].is_alive():
            for w in session.workers:
                if w is not None:
                    w.close()
            active["thread"].join(2*session.config["termination_seconds"]+5)
        if active is None or not active["thread"].is_alive():
            session.close()
        else:
            # Process exit releases SQLite and OS ownership; child sentinel kills
            # any descendant whose termination acknowledgement was uncertain.
            os._exit(73)


def parser():
    p=argparse.ArgumentParser(description="I-01 finite research stages; no automatic progression")
    p.add_argument("--source",type=Path,default=Path(__file__).parents[2])
    p.add_argument("--run",type=Path)
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("serve")
    init=sub.add_parser("init"); init.add_argument('--prior',type=Path,action='append',default=[])
    init.add_argument('--independent',action='store_true',help='Explicit new independent study; never resets an existing campaign')
    continuation=sub.add_parser('continue-checkpoint')
    continuation.add_argument('selected',type=Path)
    continuation.add_argument('--prior',type=Path,action='append',default=[])
    continuation.add_argument('--tail',choices=['latest','unknown'],required=True)
    continuation.add_argument('--evidence',required=True)
    restore=sub.add_parser("restore"); restore.add_argument("selected",type=Path); restore.add_argument("--tail",choices=["latest","unknown"],required=True); restore.add_argument("--evidence",required=True)
    check=sub.add_parser("selfcheck"); check.add_argument("--metadata",type=Path)
    inventory=sub.add_parser("runtime-inventory"); inventory.add_argument("--output",type=Path,required=True)
    for name in ("status","report"):
        item=sub.add_parser(name)
        if name=="report":
            item.add_argument("--output",type=Path)
            item.add_argument('--no-plots',action='store_true',help='Export read-only tables/traces/HTML without importing Matplotlib')
    for name in ("metadata","weights"):
        item=sub.add_parser(name); item.add_argument("--scratch",type=Path,required=True); item.add_argument("--working",type=Path,required=True)
    stage=sub.add_parser("action"); stage.add_argument("action"); stage.add_argument("--args",default="{}"); stage.add_argument("--deadline",required=True); stage.add_argument("--allowance-evidence",required=True); stage.add_argument("--authorize",required=True)
    return p


def main(argv=None):
    args=parser().parse_args(argv)
    config=json.loads((args.source/"configs/i01-course.json").read_text())
    if args.command=="runtime-inventory":
        from .setup import runtime_inventory
        result=runtime_inventory(args.source); atomic_json(args.output,result)
    elif args.command in ("metadata","weights"):
        from .setup import download
        result=download(args.source,args.scratch,args.working,weights=args.command=="weights")
    elif args.command=="init":
        from .workflow import initialize
        if args.independent and args.prior:
            raise ValueError('Independent rerun must not import prior checkpoints')
        result=initialize(args.run,args.source,config,independent=args.independent)
        if args.prior:
            from .workflow import Session
            from .continuation import record_prior_preparation
            session=Session(args.run,args.source)
            try:record_prior_preparation(args.run,session.stores,args.prior)
            finally:session.close()
    elif args.command=='continue-checkpoint':
        from .continuation import continue_checkpoint
        result=continue_checkpoint(args.selected,args.run,args.source,prior_checkpoints=args.prior,
                                   tail=args.tail,evidence=args.evidence)
    elif args.command=="restore":
        from .workflow import Session
        receipt=extract_selected(args.selected,args.run)
        session=Session(args.run,args.source)
        try:
            restore_tail(session.meta,args.tail,args.evidence,boundary=receipt['created_at'])
            result=dict(restored=receipt,continuation_requires_current_session_reload=True,tail=args.tail)
        finally:
            session.close()
    elif args.command=="selfcheck":
        from .checks import run_checks
        result=run_checks(args.metadata,config)
    elif args.command in ("status","report"):
        from .report import analysis, write_report
        result=analysis(args.run)["summary"] if args.command=="status" else write_report(args.run,args.output or args.run/"reports",plot=not args.no_plots)
    elif args.command=="serve":
        serve(args.run,args.source); return
    else:
        from .workflow import Session
        # One-shot calls close models; use serve/client for resident inference.
        session=Session(args.run,args.source,progress=lambda e:print(canonical(e),flush=True))
        try:
            session.window(args.deadline,args.allowance_evidence)
            session.meta.put_meta("operator_authorization",dict(action=args.action,evidence=args.authorize))
            result=session.run_action(args.action,**json.loads(args.args))
        finally:
            session.close()
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
