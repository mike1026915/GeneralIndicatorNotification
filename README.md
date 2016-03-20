# GeneralIndicatorNotification
This is a auto-notification tool for any indicator on the Internet that you want to oberseve

## Usage ##
1. Download to your machine
2. Rename receiver_config.json.example to receiver_config.json
3. Rename data_config.json.example to data_config.json
4. In data_config.json, you have to write the URL and the xpath for the indicator. If the data downloaded from the URL is not HTML, you have to define your parser in parser_method.py
5. In receiver_config.json, you have to specify the notofication method and necessary token for sending notification
6. You can execute "python main.py" to check the fetched value and test the push notification result
7. Set the cronjob to trigger this script periodically

### data_config.json ###
```json
[
    {
        "url": "http://rate.bot.com.tw/Pages/Static/UIP003.zh-TW.htm",
        "indicators":
        [
            {
                "name": "JPY in Bank of Taiwan",
                "xpath": ".//*[@id='slice1']/div[2]/table[2]/tr[10]/td[2]",
                "condition": "< 0.30",
                "message": "JPY "
            },
            {
                "name": "USD in Bank of Taiwan",
                "xpath": "//*[@id='slice1']/div[2]/table[2]/tr[3]/td[2]",
                "condition": "< 35",
                "message": "USD is less than 30 dollars "
            }
        ]
    },
    {
        "url": "http://example.com/get_special_format_data",
        "indicators":
        [
            {
                "name": "Sample",
                "parser": "sample_parser",
                "condition": "> 50",
                "message": "Just a test"
            }
        ]

    }
]

```
   * "name" is the indicator name that we will use later.
   * "xpath" is the xpath of the indicator on the web page
   * "condition" is the criteria
      * Condition format should be <operator> <operand> (([&|]) <operator> <operand>)*
      * <operator> includes python operator ('>', '<', '>=', '<=', '==', '!=', 'in')
      * Example: "< 35", "> 50 & < 100"
   * "message" would show in the notification
   * "parser" is the parser function name in the push_methods.py. In the function, you will get the URL content and you should return a value(no matter it is a string , an int or a float)

### receiver_config.json ###
```json
[
    {
        "name":"User1",
        "push_method":"qpush",
        "credentials":{
            "device_name":"",
            "device_pushcode":""
        },
        "monitor_indicators": [
            "JPY in Bank of Taiwan"
        ]
    },
    {
        "name":"User2",
        "push_method":"pushbullet",
        "credentials":{
            "access_token":""
        },
        "monitor_indicators": [
            "USD in Bank of Taiwan"
        ]
    }
]
```
  * "name" is the user name that received notification
  * "push_method" is the push notification method you use. Currently , we provied "qpush" and "pushbullet" two methods. You can also define your own method in push_methods.py. You have to register an account the get the token to use these methods
    * "qpush": https://qpush.me/zh_tw/
    * "pushbullet": https://www.pushbullet.com/
  * "credentials" means the token you registed
  * "monitor_indicators" is the indicator name defined in data_config.jsonyou would like to receive the notification
  * If you would like to define your own push method, just follow the format in the push_method.py, Define a function that get two parameters, user and msg, then send the message you like in your method

