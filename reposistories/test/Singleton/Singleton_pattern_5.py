class Configuration:
    def __init__(self, setting="default"):
        self.setting = setting
_global_config_instance = Configuration("initial_setting")
def get_config_singleton():
    return _global_config_instance
c1 = get_config_singleton()
c2 = get_config_singleton()
assert c1 is c2
assert c1.setting == "initial_setting"
c1.setting = "new_setting"
assert c2.setting == "new_setting"