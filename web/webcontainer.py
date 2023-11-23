import threading


class _MainWebContent():

    def __init__(self):
        self.services = {}
        self.lock = threading.Lock()

    def push(self,service):
        self.lock.acquire()
        try:
            self.services[service.url] = service
        finally:
            self.lock.release()

    def pop(self,service_name):
        self.lock.acquire()
        try:
            p = self.services.pop(service_name)
        finally:
            self.lock.release()
        return p

    def delete(self,service_name):
        self.lock.acquire()
        try:
            self.services.pop(service_name)
        finally:
            self.lock.release()

    def get(self,service_name):
        return self.services[service_name]

    def clear(self):
        self.lock.acquire()
        try:
            self.services.clear()
        finally:
            self.lock.release()

    def get_names(self):
        return list(self.services.keys())


web_content = _MainWebContent()









