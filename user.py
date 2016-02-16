class User(object):
    def __init__(self, json_object):
        self.name = json_object['name']
        self.push_method = json_object['push_method']
        self.credentials = json_object['credentials']
        self.monitor_indicators = json_object['monitor_indicators']