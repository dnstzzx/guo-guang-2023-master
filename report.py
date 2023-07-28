from dataclasses import dataclass
from typing import Callable, Dict, List, Set
from promise import Promise
from threading import Lock

@dataclass
class Report:
    name: str
    args: List[str]

report_listeners: Dict[str, Set[Callable[[Report], None]]] = {}
report_promises: Dict[str, List[Promise[Report]]] = {}
promise_lock = Lock()

def add_report_listener(rpt_name: str, listener: Callable[[Report], None]):
    if rpt_name not in report_listeners.keys():
        report_listeners[rpt_name] = set([])
    report_listeners[rpt_name].add(listener)

def remove_report_listener(rpt_name: str, listener: Callable[[Report], None]):
    if rpt_name not in report_listeners.keys():
        report_listeners[rpt_name].remove(listener)

def add_report_promise(rpt_name: str, promise: Promise[Report]):
    with promise_lock:
        if rpt_name not in report_promises.keys():
            report_promises[rpt_name] = []
        report_promises[rpt_name].append(promise)

def on_report_recv(rpt: Report):
    name = rpt.name
    if name in report_listeners.keys():
        for listener in report_listeners[name]:
            listener(rpt)

    with promise_lock:
        promises = report_promises.pop(name, [])

    for promise in promises:
        promise.set_done(rpt)
    