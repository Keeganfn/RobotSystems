from readerwriterlock import rwlock

class MessageBus():

    def __init__(self) -> None:
        self.lock = rwlock.RWLockWriteD()
        self.msg = None

    def write(self, msg):
        with self.lock.gen_wlock():
            self.msg = msg

    def read(self):
        with self.lock.gen_rlock():
            return self.msg