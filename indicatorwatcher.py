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
        #full_condition = result_value + condition
        #return eval(full_condition)
        tokens = condition.split()
        result = True
        relation_operator = '&'
        OPERATOR = ('>', '<', '>=', '<=', '==', '!=', 'in')
        try:
            float(result_value)
        except ValueError:
            result_value = "'" + str(result_value) + "'"
        exp_list = [result_value]
        RELATION_OPERATOR = ('|', '&')
        if (len(tokens) - 2) % 3 != 0:
            print "Format error, token number is weird"
            return False
        for i, token in enumerate(tokens):
            if i % 3 == 0:  # First element should be operator
                if token not in OPERATOR:
                    print "Format error, operator error"
                    return False
                exp_list.append(token)
            elif i % 3 == 1:  # Second element should be operand
                exp_list.append(token)
                statement = ' '.join(exp_list)
                try:
                    if relation_operator == '&':
                        result = result and eval(statement)
                    elif relation_operator == '|':
                        result = result or eval(statement)
                    else:
                        print "Format error, relation operator error"
                        return False
                except BaseException as e:
                    print "Format error,statement, %s,  error, %s" % (statement, str(e))
            elif i % 3 == 2:
                if token not in RELATION_OPERATOR:
                    print "Format error, relation operator error"
                    return False
                relation_operator = token
                exp_list = [result_value]
        return result

    def execute(self):
        result_list = []
        for web in self._config_data:
            tree = self._get_web_page_etree(web['url'])
            for indicator in web['indicators']:
                find_list = self._get_xpath_result(tree, indicator['xpath'])
                if len(find_list) == 0:
                    message =  "It doesn't find anything based on the given xpath. Please check the xpath"
                    print message
                    result_list.append({'name': name, 'value': "N/A", 'message': message})
                    continue
                for result in find_list:
                    try:
                        if self._eval_condition(result.text, indicator['condition'].strip()):
                            name = indicator['name']
                            message = indicator['message']
                            result_list.append({'name': name, 'value': result.text, 'message': message})
                    except BaseException as e:
                        print "Unexpected Error. %s" % str(e)
        return result_list

if __name__ == "__main__":
    iw = IndicatorWatcher('data_config.json')
    tree = iw._get_web_page_etree('http://rate.bot.com.tw/Pages/Static/UIP003.zh-TW.htm')
    print iw._get_xpath_result(tree, "//*[@id='slice1']/div[2]/table[2]/tr[3]/td[2]")
    assert IndicatorWatcher('data_config.json')._eval_condition("5", "< 10") == True, "Test case1"
    assert IndicatorWatcher('data_config.json')._eval_condition("5", "< 10 & >= 1") == True, "Test case2"
    assert IndicatorWatcher('data_config.json')._eval_condition("abc", "== 'abc'") == True, "Test case3"
    assert IndicatorWatcher('data_config.json')._eval_condition("a", "in 'abc'") == True, "Test case4"
    assert IndicatorWatcher('data_config.json')._eval_condition("15", "< 20 | > 15") == True, "Test case5"
