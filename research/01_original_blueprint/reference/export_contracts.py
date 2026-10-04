"""Export reviewed schemas and worked examples. Run after tests."""
import hashlib
import json
from pathlib import Path
from . import contracts as c
from .support import atom, AND, OR, Obs, labels, serialize


def canonical(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    schemas, examples = root / "schemas", root / "examples"
    schemas.mkdir(exist_ok=True); examples.mkdir(exist_ok=True)
    classes = [v for v in vars(c).values() if isinstance(v, type) and issubclass(v, c.Strict) and v is not c.Strict]
    schemas_data = {cls.__name__: cls.model_json_schema() for cls in classes}
    (schemas/"contracts.schema.json").write_text(json.dumps(schemas_data, indent=2)+"\n")

    reply = c.AgentReply(ack_epoch=1, claims=[c.ClaimDraft(slot="feasible:target", value=True, refs=["y@1", "p@1"])],
        actions=[c.ActionCommand(operation="new", target_action_id="a1",
                 proposal=c.ActionDraft(job="target", verb="dispatch", resource="Y", refs=["y@1", "p@1"]))])
    plan = c.RepairPlan(policy="O", correction_id="corr1", withdraw_claims=("cx",), suspend_actions=("a1",), notices=("cx", "a1"), mask_source="oracle")
    ex = c.ExtractorReply(supports=[c.ExtractedNode(n="q", j=(("x@1","p@1"),("y@1","p@1"))),
                                   c.ExtractedNode(n="a1", j=(("x@1","p@1"),))])
    for name, value in [("agent_reply.json", reply), ("repair_plan.json", plan), ("extractor_reply.json", ex)]:
        (examples/name).write_text(value.model_dump_json(indent=2)+"\n")

    f = AND(atom("permit"), OR(atom("x"), atom("y")))
    before={"permit":Obs("p@1",True),"x":Obs("x@1",True),"y":Obs("y@1",True)}
    after={**before,"x":Obs("x@2",False)}
    demo={"formula":f.model_dump(),"claim_before":serialize(labels(f,True,before)),
          "claim_after":serialize(labels(f,True,after)),
          "dispatch_X_after":serialize(labels(AND(atom("permit"),atom("x")),True,after)),
          "dispatch_Y_after":serialize(labels(AND(atom("permit"),atom("y")),True,after)),
          "not_an_llm_experiment":True}
    (examples/"worked_support.json").write_text(json.dumps(demo,indent=2)+"\n")

    payload=plan.model_dump(mode="json")
    base=dict(schema_version="1.0",event_id="ev1",branch_id="demo.O",seq=1,epoch=1,logical_step=5,actor="SYSTEM",kind="repair_plan",payload=payload,previous_sha256="0"*64)
    event=c.Event(**base,sha256=digest(base))
    c.validate_event_payload(event)
    (examples/"event.json").write_text(event.model_dump_json(indent=2)+"\n")
    print(json.dumps({"schema_models":len(classes),"examples":5,"status":"generated_and_validated"}))


if __name__ == "__main__":
    main()
