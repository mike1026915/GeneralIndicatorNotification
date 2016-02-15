import json
import urllib2
from lxml import etree


class IndicatorWatcher(object):
    def __init__(self, indicator_config):
        with open(indicator_config) as config_file:
            self._config_data = json.load(config_file)

    def execute(self):
        result_list = []
        for web in self._config_data:
            response = urllib2.urlopen(web['url'])
            htmlparser = etree.HTMLParser()
            tree = etree.parse(response, htmlparser)
            for indicator in web['indicators']:
                xpath = indicator['xpath']
                find_list = tree.xpath(xpath)
                if find_list:
                    try:
                        value = float(find_list[0].text)
                        condition = indicator['condition']
                        full_condition = str(value) + condition
                        if eval(full_condition):
                            name = indicator['name']
                            message = indicator['message']
                            result_list.append({'name': name, 'value': value, 'message': message})
                    except ValueError:
                        print "Value error, %s is not a digit" % find_list[0].text
                    except BaseException as e:
                        print "Unexpected Error. %s" % str(e)
                else:
                    print "It doesn't find anything based on the given xpath"
        return result_list
