import json
from push_methods import SEND_METHOD

class NotifierFactory(object):
    @staticmethod
    def getSender(push_method):
        if push_method in SEND_METHOD:
            return SEND_METHOD[push_method]
        else:
            raise NotImplementedError("This push method is not registered.")


class Notifier(object):
    def __init__(self, receiver_config):
        self._receiver_config = self._parse_config(receiver_config)

    def _parse_config(self, receiver_config):
        raise NotImplementedError("Todo")

    def process_queue(self, message_queue):
        # msg
        # NotifierFactory.getSender(method)(msg)
        raise NotImplementedError("Todo")