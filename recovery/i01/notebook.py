"""Named, finite research steps for ordinary notebook cells.

The existing operator owns presentation and the retained controller. These
methods expose its actual research stages rather than string UI commands.
"""
from .ui import Operator


class Study(Operator):
    def start_new(self):
        """Explicit fresh rerun; retain the window observed before preparation."""
        return self.open('new',independent=True,deadline=self.deadline,
                         allowance_evidence=self.allowance_evidence or '')
    def install_runtime(self): return self.run('setup')
    def open(self, mode='new', **session_facts): return self.open_study(mode,**session_facts)
    def set_session_window(self, deadline, evidence): return self.run('window',deadline=deadline,evidence=evidence)
    def configure_session(self, *, remaining_minutes=None, deadline=None, evidence='', refresh=False, basis='operator_observed'):
        return self.run('window',deadline=deadline,evidence=evidence,remaining_minutes=remaining_minutes,refresh=refresh,basis=basis)
    def record_state_review(self, notes):return self.run('review',scope='readiness',notes=notes)
    def check_implementation(self): return self.run('selfcheck')
    def download_weights(self): return self.run('weights')
    def load_models(self): return self.run('load')
    def check_readiness(self, *, reload=False): return self.run('readiness',**({'reload':True} if reload else {}))
    def run_diagnostics(self):return self.run('diagnostics')
    def qualify_direct(self): return self.run('screen',mode='direct')
    def inspect_qualification(self, mode=None): return self.inspect(worlds=[f'qualification-{i:02d}' for i in range(4 if self.assisted else 6)],qualification_mode=mode,audit_limit=3)
    def inspect_thinking(self): return self.inspect_qualification('thinking')
    def qualify_thinking(self, reason=None): return self.thinking_screen(reason)
    def check_headroom(self, *, reload=False): return self.envelope(reload=reload)
    def plan_execution(self):return self.run('plan_execution')
    def check_pilot(self, number):return self.run('check_pilot',number=number)
    def admit_main(self):return self.run('admit_main')
    def run_pilot(self, number): return self.run('pilot',number=number)
    def record_pilot_review(self, number, **findings): return self.review_pilot(number,**findings)
    def review_configuration(self): return self.preview_freeze()
    def freeze_configuration(self, notes): return self.run('freeze',notes=notes)
    def prepare_main_batch(self, count=2): return self.run('prepare_batch',count=count)
    def run_main_batch(self, number=None):
        return self.run_batch() if number is None else self.run('automatic_main',number=number)
    def record_batch_review(self, notes=''): return self.review_batch(notes)
    def build_report(self): return self.final_report()
    def save_checkpoint(self, *, verify=False):
        result=self.run('snapshot')
        if verify:
            try:self.verify_checkpoint()
            except Exception as error:
                self.operation_error('verify_checkpoint',error)
                raise
        return result
    def show_status(self): return self.run('status')
    def pause(self): return self.run('pause')
    def finish_session(self):
        self.run('close_models')
        return self.run('shutdown')
    def reconcile_attempt(self, slot, attempt, evidence):
        return self.client.command('reconcile',slot=slot,attempt=attempt,evidence=evidence)
    def confirm_timeout_termination(self, slot, call, evidence):
        return self.client.command('confirm_timeout_termination',slot=slot,call=call,evidence=evidence)
    def record_lost_spending(self, gap, affected_worlds=None):
        return self.client.command('lost_spending',gap=gap,affected_worlds=affected_worlds or [])
    def resolve_restore_tail(self, upper, evidence, affected_worlds=None):
        return self.client.command('resolve_restore_tail',upper=upper,evidence=evidence,affected_worlds=affected_worlds or [])
