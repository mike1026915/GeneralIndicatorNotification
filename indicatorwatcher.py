import json
import urllib2
from lxml import etree


class IndicatorWatcher(object):
    def __init__(self, indicator_config):
        with open(indicator_config) as config_file:
            self._config_data = json.load(config_file)

    def _get_web_page_etree(self,url):
        """
            Given url, it returns the etree object
        """
        response = urllib2.urlopen(url)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        return tree

    def _get_xpath_result(self, tree, xpath):
        """
            It returns the element list speicified by xpath in the xml tree
        """
        return tree.xpath(xpath)

    def _eval_condition(self, result_value, condition):
        full_condition = result_value + condition
        return eval(full_condition)

    def execute(self):
        result_list = []
        for web in self._config_data:
            tree = self._get_web_page_etree(web['url'])
            for indicator in web['indicators']:
                find_list = self._get_xpath_result(tree, indicator['xpath'])
                for result in find_list:
                    try:
                        if self._eval_condition(result.text, indicator['condition']):
                            name = indicator['name']
                            message = indicator['message']
                            result_list.append({'name': name, 'value': result.text, 'message': message})
                    except BaseException as e:
                        print "Unexpected Error. %s" % str(e)
                else:
                    print "It doesn't find anything based on the given xpath"
        return result_list

if __name__ == "__main__":
    assert IndicatorWatcher('data_config.json')._eval_condition("5", "< 10") == True, "Test case1"
    assert IndicatorWatcher('data_config.json')._eval_condition("5", "< 10 & >= 1") == True, "Test case2"
    assert IndicatorWatcher('data_config.json')._eval_condition("abc", "== 'abc'") == True, "Test case3"
    assert IndicatorWatcher('data_config.json')._eval_condition("a", "in 'abc'") == True, "Test case4"
    assert IndicatorWatcher('data_config.json')._eval_condition("15", "< 20 | > 15") == True, "Test case5"
