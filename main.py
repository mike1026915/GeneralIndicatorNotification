from indicatorwatcher import IndicatorWatcher
from notifier import Notifier
if __name__ == "__main__":
    to_be_notified = IndicatorWatcher("data_config.json").execute()
    print "to_be_notified", to_be_notified
    if to_be_notified:
        Notifier('receiver_config.json').process_queue(to_be_notified)



