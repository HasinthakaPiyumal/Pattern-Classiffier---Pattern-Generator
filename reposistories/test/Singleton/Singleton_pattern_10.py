class Borg:
    _shared_state = {}
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj
    def __init__(self, value=None):
        if not hasattr(self, 'initialized_borg_state'):
            self.initialized_borg_state = True
            self.value = value if value is not None else "default borg value"
b1 = Borg("first_borg_value")
b2 = Borg("second_borg_value")
b3 = Borg()
assert b1 is not b2
assert b1.value == "first_borg_value"
assert b2.value == "first_borg_value"
assert b3.value == "first_borg_value"
b1.value = "changed_borg_value"
assert b2.value == "changed_borg_value"
assert b3.value == "changed_borg_value"
b2.new_attribute = "added_by_b2"
assert b1.new_attribute == "added_by_b2"
assert b3.new_attribute == "added_by_b2"