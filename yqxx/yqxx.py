import argparse
import base64
import json
import logging
import random
import re
import traceback
import urllib
from datetime import date
from typing import Tuple

import requests
import yaml
from bs4 import BeautifulSoup
from hit.ids.login import idslogin

logging.basicConfig(level=logging.INFO)


def read_config(filename: str) -> Tuple[str, str, str, str, str, str]:
    try:
        logging.info("Reading config from %s" % filename)
        o = open(filename, 'r')
        c = yaml.load(o, Loader=yaml.SafeLoader)
        if 'dqztm' not in c:
            c['dqztm'] = '01'
        if 'dqszdqu' not in c:
            c['dqszdqu'] = '230103'
        ret = (c['username'], c['password'], c['brzgtw'],
               c['gnxxdz'], c['dqztm'], c['dqszdqu'])
        return ret
    except OSError:
        logging.error('Fail to read configuration from %s' % filename)
    except yaml.YAMLError:
        logging.error('Fail to parse YAML')
    exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog='yqxx', description='Auto submitter for xg.hit.edu.cn yqxx')
    parser.add_argument('-c', '--conf-file',
                        help='Set config file path', required=True)
    args = parser.parse_args()
    (username, password, brzgtw,
     gnxxdz, dqztm, dqszdqu) = read_config(args.conf_file)
    logging.info('Logging in to xg.hit.edu.cn')
    try:
        s = idslogin(username, password)
    except Exception as e:
        logging.error('Failed while logging in')
        logging.error(e)
        exit(1)
    # s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36'
    })
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common')
    _ = urllib.parse.urlparse(r.url)
    if _.hostname != 'xg.hit.edu.cn':
        logging.error('Login failed')
        exit(1)
    logging.info('Login success')
    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/csh')
    _ = json.loads(r.text)
    if _['isSuccess'] == True:
        module = _['module']
        logging.info("Successfully created yqxx")
        logging.debug("yqxx id: %s" % module)
    else:
        module = ''
        r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/getYqxxList')
        yqxxlist = json.loads(r.text)
        if yqxxlist['isSuccess'] == False:
            logging.error(
                'Fail to getYqxxList, msg: %s' % yqxxlist['msg'])
            exit(1)
        yqxxlist = yqxxlist['module']['data']
        for i in yqxxlist:
            if i['rq'] == date.today().isoformat():
                logging.info('Find previously created yqxx.')
                if i['zt'] != '00':
                    # 已提交
                    # Don't need to do anything
                    logging.error("You have already submitted yqxx, EXITING!")
                    exit(0)
                else:
                    module = i['id']
                    logging.info("Using previously created yqxx")
                    logging.debug("yqxx id: %s" % module)
                    break
    if not module:
        logging.error('Could not find yqxx!')
        exit(1)
    data = {
        'info': json.dumps({
            "model": {
                "id": module,
                "brfsgktt": "0",  # 发烧、干咳、头痛现象
                "brjyyymc": "",  # 医院名称
                "brsfjy": "",  # 是否就医
                "brzdjlbz": "",  # 诊断结论备注
                "brzdjlm": "",  # 诊断结论
                "brzgtw": brzgtw,  # 体温
                "dqszd": "01",  # 01 国（境）内, 02 海外
                "dqszdqu": dqszdqu,  # 当前所在区
                "dqszdsheng": str(dqszdqu[:2]) + '0000',  # 当前所在省
                "dqszdshi": str(dqszdqu[:4]) + '00',  # 当前所在市/县
                "dqztbz": "",  # 备注
                "dqztm": dqztm,  # 当前状态 01 在校（校内宿舍住）, 03 居家, 04 探亲, 05 访友, 06 旅行, 07 会议, 99 其他
                "gnxxdz": gnxxdz,  # 国（境）内详细地址
                "gpsxx": "",  # GPS
                "hwcs": "",  # 海外城市
                "hwgj": "",  # 海外国家
                "hwxxdz": "",  # 海外详细地址
                "qtbgsx": "",  # 其他需要报告的事项
                "sffwwhhb": "0",  # 上次填报至今到访高危地区？
                "sfjcqthbwhry": "0",  # 其他接触高危地区人员的情况描述
                "sfjcqthbwhrybz": "",  # 其他接触高危地区人员的情况描述
                "sfjdwhhbry": "0",  # 是否接待过从高危地区来的朋友、亲属或同学
                "sftjwhjhb": "0",  # 上次填报至今是否途经高危地区？
                "sftzrychbwhhl": "0",  # 同住人员是否有从高危地区回来的
                "tccx": "",  # （同程）车厢号
                "tchbcc": "",  # （同程）航班号/车次
                "tcjcms": "",  # （同程）接触描述
                "tcjtfsbz": "",  # （同程）交通方式备注
                "tcjtfs": "",  # （同程）交通方式
                "tcyhbwhrysfjc": "0",  # 未进出高危地区但与高危地区人员有接触情况
                "tczwh": ""  # （同程）座位号
            }
        })
    }
    logging.debug("data: %s" % data['info'])
    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/saveYqxx', data=data)
    logging.debug(r.text)
    j = json.loads(r.text)
    if j['isSuccess'] == True:
        logging.info("saveYqxx: Success")
    else:
        logging.error("saveYqxx: Failed")
        exit(1)
    logging.debug(j)
    return


if __name__ == "__main__":
    main()
