# -*- coding: utf-8 -*-
import re


def bsp_mma_parser_USD(response):
    reg_pattern = r'genREMITResult.+\(USD\)","DataValue1Img":".+","DataValue2":".+","DataValue3":"(.+)","DataValue4":"USD".+'
    match = re.search(reg_pattern, response)  
    if match is not None:
        return match.group(1)
    else:
        return None

def bsp_mma_parser_JPY(response):
    reg_pattern = r'genREMITResult.+\(JPY\)","DataValue1Img":".+","DataValue2":".+","DataValue3":"(.+)","DataValue4":"JPY".+'
    match = re.search(reg_pattern, response)
    if match is not None:
        return match.group(1)
    else:
        return None

