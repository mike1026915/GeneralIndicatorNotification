from indicatorwatcher import IndicatorWatcher
from notifier import Notifier
if __name__ == "__main__":
    to_be_notified = IndicatorWatcher("data_config.json").execute()
    print to_be_notified
    if to_be_notified:
        Notifier(to_be_notified, 'receiver_config.json').send()



