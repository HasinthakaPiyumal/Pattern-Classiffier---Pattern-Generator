class Target:
    def request(self):
        return "Target request"

class Adaptee:
    def specific_request(self):
        return "Adaptee specific request"

class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    def request(self):
        return self.adaptee.specific_request()
