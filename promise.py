from threading import Lock, Condition
from typing import Generic, TypeVar, List, Callable


T = TypeVar('T')
class Promise(Generic[T]):
    data: T
    def __init__(self) -> None:
        self.data = None
        self._done = False
        self._callbacks: List[Callable[[T], None]] = []
        self._lock = Lock()
        self._notifier = Condition(self._lock)
        
    def is_done(self) -> bool:
        return self._done

    def set_done(self, data: T = None):
        if self._done:
            return

        with self._lock:
            self._done = True
            self.data = data

        for listener in self._callbacks:
            listener(data)
        
        with self._notifier:
            self._notifier.notify_all()

    def add_callback(self, callback: Callable[[T], None]):
        if self._done:
            callback(self.data)
            return

        with self._lock:
            if self._done:
                callback(self.data)
                return
            self._callbacks.append(callback)
    
    def wait(self) -> T:
        if self._done:
            return self.data

        with self._notifier:
            if self._done:
                return self.data
            self._notifier.wait()
    
    @staticmethod
    def all(promises: List['Promise']) -> 'Promise':
        count = len(promises)
        dones = [False for i in range(count)]
        datas = [None for i in range(count)]
        joined_promise = Promise()

        def check_all_done():
            for done in dones:
                if not done:
                    return
            joined_promise.set_done(datas)

        for i in range(count):
            promise = promises[i]
            def gen_callback(i):
                def callback(data):
                    dones[i] = True
                    datas[i] = data
                    check_all_done()
                return callback
            promise.add_callback(gen_callback(i))

        return joined_promise