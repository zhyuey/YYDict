# -*- coding: utf-8 -*-
import sys
import requests
import json


class YoudaoDict:
    url_1 = 'http://fanyi.youdao.com/openapi.do'
    data = {
	'keyfrom': 'YYDict',
	'key': '1662649610',
	'type': 'data',
	'doctype': 'json',
	'version': 1.1,
	'q': ''	}
    @staticmethod
    def searchDict(word):
        url = YoudaoDict.url_1
        YoudaoDict.data['q'] = word
        resp = requests.get(url, params=YoudaoDict.data)
        content = resp.text
        rt_text = ''
        if content:
            strct = json.loads(content)
            if strct['errorCode'] == 0:
                rt_text = strct['query']
                rt_text += '\n'
                rt_text += '———————————————————————————————\n\n'
                basic = strct.get('basic', '')
                if len(basic) > 0:
                    exp = basic.get('explains')    
                    for ex in exp:
                        rt_text += ex
                        rt_text += '\n'
                web = strct.get('web', '')
                if len(web) > 0:
                    rt_text += '\n————————————— 网络释义 —————————————\n\n'
                    for listval in web:
                        rt_text += listval.get('key', '')
                        rt_text += ' | '
                        mval=','.join(listval.get('value', ''))
                        rt_text += mval
                        rt_text += '\n'


        return rt_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        sys.exit(0)
    rtstr = YoudaoDict().searchDict(word)
    print(rtstr)
