# -*- coding: utf-8 -*-
import sys
import requests
import json


class BaiduDict:
    url_1 = 'http://apis.baidu.com/apistore/tranlateservice/dictionary?query='
    url_2 = '&from=en&to=zh'
    headers = {"apikey": "5035fad4bdc3e6b76ad704a2dc797299"}

    @staticmethod
    def searchDict(word):
        url = BaiduDict.url_1 + word + BaiduDict.url_2
        resp = requests.get(url, headers=BaiduDict.headers)
        content = resp.text
        rt_text = ''
        if content:
            print(content)
            strct = json.loads(content)
            if strct['errNum'] != 0:
                rt_text += content['errMsg']
                rt_text += '\n'
            result = strct['retData']['dict_result']
            if not isinstance(result, list):
                rt_text += result['word_name']
                rt_text += '\n'
                rt_text += '———————————————————————————————\n'
                rt_text += '\n'
                parts = result['symbols'][0]['parts']
                for part in parts:
                    if 'part' in part:
                        partval = part.get('part', '')
                        rt_text += partval
                        rt_text += '\n'
                        for mean in part['means']:
                           rt_text += mean
                           rt_text += '\n'
                    if 'part_name' in part:
                        part_nameval = part.get('part_name', '')
                        rt_text += part_nameval
                        rt_text += '\n'
                        for mean in part['means']:
                            rt_text += mean.get('word_mean', '')
                            rt_text += '\n'
        return rt_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        sys.exit(0)
    rtstr = BaiduDict().searchDict(word)
    print(rtstr)
