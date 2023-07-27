from dataclasses import dataclass
from typing import Callable, Dict, List

@dataclass
class Report:
    name: str
    args: List[str]

report_listeners: Dict[str, set[Callable[[Report], None]]] = {}

def add_report_listener(rpt_name: str, listener: Callable[[Report], None]):
    if rpt_name not in report_listeners.keys():
        report_listeners[rpt_name] = set([])
    report_listeners[rpt_name].add(listener)

def remove_report_listener(rpt_name: str, listener: Callable[[Report], None]):
    if rpt_name not in report_listeners.keys():
        report_listeners[rpt_name].remove(listener)
