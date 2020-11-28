import argparse
import base64
import json
import logging
import random
import re
import urllib
from datetime import date

import requests
import yaml
from bs4 import BeautifulSoup

from .utils import encrypt, rds

logging.basicConfig(level=logging.INFO)


def read_config(filename: str):
    try:
        logging.info("Reading config from %s" % filename)
        o = open(filename, 'r')
        c = yaml.load(o, Loader=yaml.SafeLoader)
        ret = (c['username'], c['password'], c['brzgtw'], c['gnxxdz'])
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
    (username, password, brzgtw, gnxxdz) = read_config(args.conf_file)
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36'
    })
    # Login via ids.hit.edu.cn
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common')
    logging.info('Logging in to xg.hit.edu.cn')
    pwd_default_encrypt_salt = re.compile(
        'pwdDefaultEncryptSalt = "(.*)"').search(r.text).groups()[0]
    logging.debug('pwdDefaultEncryptSalt: %s' % pwd_default_encrypt_salt)
    passwordEncrypt = encrypt(
        rds(64).encode()+password.encode(), pwd_default_encrypt_salt.encode())
    logging.debug(passwordEncrypt.decode())
    soup = BeautifulSoup(r.text, 'html.parser')
    # Detect Captcha
    _ = s.get('http://ids.hit.edu.cn/authserver/needCaptcha.html?username=%s&pwdEncrypt2=pwdEncryptSalt' % username)
    if _.text == 'true':
        logging.error('Fail: Captcha needed')
        exit(1)
    logging.info('OK: No captcha is needed')
    r = s.post(r.url, data={
        "username": username,
        "password": passwordEncrypt,
        "captchaResponse": None,
        "lt": soup.find('input', {'name': 'lt'})['value'],
        "dllt": soup.find('input', {'name': 'dllt'})['value'],
        "execution": soup.find('input', {'name': 'execution'})['value'],
        "_eventId": soup.find('input', {'name': '_eventId'})['value'],
        "rmShown": soup.find('input', {'name': 'rmShown'})['value'],
        "pwdDefaultEncryptSalt": pwd_default_encrypt_salt
    })
    _ = urllib.parse.urlparse(r.url)
    if _.hostname != 'xg.hit.edu.cn':
        logging.error('Login failed')
        exit(1)
    logging.info("Login success")
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
                "dqszdqu": "230103",  # 当前所在区
                "dqszdsheng": "230000",  # 当前所在省
                "dqszdshi": "230100",  # 当前所在市/县
                "dqztbz": "",  # 备注
                "dqztm": "01",  # 当前状态 01 在校（校内宿舍住）, 03 居家, 04 探亲, 05 访友, 06 旅行, 07 会议, 99 其他
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
