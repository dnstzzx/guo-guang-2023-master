from typing import Callable
from promise import Promise
import report

class Button:
    def __init__(self, report_name: str) -> None:
        self.report_name = report_name

    def add_released_listener(self, callback: Callable[[report.Report], None]):
        report.add_report_listener(self.report_name, callback)

    def remove_released_listener(self, callback: Callable[[report.Report], None]):
        report.remove_report_listener(self.report_name, callback)

    def add_released_promise(self, promise: Promise):
        report.add_report_promise(self.report_name, promise)

    def wait_for_released(self):
        pms = Promise()
        self.add_released_promise(pms)
        pms.wait()


btn_mid = Button('BTN_MID')
btn_set = Button('BTN_SET')
btn_res = Button('BTN_RES')