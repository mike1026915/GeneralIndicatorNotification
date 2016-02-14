
if __name__ == "__main__":
    to_be_notified = IndicatorWatcher("data_config.json").execute()
    if to_be_notified:
        Notifier(to_be_nofied, 'receiver_config.json').send()



