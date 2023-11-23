# lock
import threading

class _MainContent():

    def __init__(self):
        self.chains = {}
        self.lock = threading.Lock()

    def push(self,chain):
        self.lock.acquire()
        try:
            self.chains[chain.chain_name] = chain
        finally:
            self.lock.release()

    def pop(self,chain_name):
        self.lock.acquire()
        try:
            p = self.chains.pop(chain_name)
        finally:
            self.lock.release()
        return p

    def delete(self,chain_name):
        self.lock.acquire()
        try:
            self.chains.pop(chain_name)
        finally:
            self.lock.release()

    def get(self,chain_name):
        return self.chains[chain_name]

    def clear(self):
        self.lock.acquire()
        try:
            self.chains.clear()
        finally:
            self.lock.release()

    def get_names(self):
        return list(self.chains.keys())


content = _MainContent()









