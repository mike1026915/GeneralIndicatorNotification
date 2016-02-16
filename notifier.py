import json
from push_methods import SEND_METHOD
from user import User

class NotifierFactory(object):
    @staticmethod
    def getSender(push_method):
        if push_method in SEND_METHOD:
            return SEND_METHOD[push_method]
        else:
            raise NotImplementedError("This push method is not registered.")


class Notifier(object):
    def __init__(self, receiver_config):
        self._indicator_watchers = dict()
        self._users = list()
        self._receiver_config = self._parse_config(receiver_config)

    def _parse_config(self, receiver_config):
        with open(receiver_config) as config_file:
            json_array = json.load(config_file)
        for user_obj in json_array:
            user = User(user_obj)
            self._users.append(user)

            for indicator in user.monitor_indicators:
                if indicator not in self._indicator_watchers:
                    self._indicator_watchers[indicator] = list()
                self._indicator_watchers[indicator].append(user)

        print self._indicator_watchers

    def process_queue(self, message_queue):
        msg_strs = dict()
        for user in self._users:
            msg_strs[user] = ""

        for msg in message_queue:
            for user in self._indicator_watchers[msg['name']]:
                msg_strs[user] += msg['message'] + "\n"

        for user, msg in msg_strs.iteritems():
            if msg != "":
                NotifierFactory.getSender(user.push_method)(user, msg)
