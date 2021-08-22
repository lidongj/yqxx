import argparse
import json
import logging
import random
import sys
import urllib
from datetime import date
from typing import Tuple

import yaml
from hit.ids.login import idslogin

logger = logging.getLogger(__name__)

USER_AGENT_LIST = [
    # OnePlus Nord Dual 5G
    'Mozilla/5.0 (Linux; Android 10; AC2001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
    # Honor V40 Lite 5G
    'Mozilla/5.0 (Linux; Android 10; ALA-AN70 Build/HONORALA-AN70; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36',
    # Huawei P40 5G
    'Mozilla/5.0 (Linux; Android 10; ANA-AN00; HMSCore 5.3.0.312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 HuaweiBrowser/11.1.1.300 Mobile Safari/537.36',
    # Huawei P40 Lite E
    'Mozilla/5.0 (Linux; Android 10; ART-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36',
    # Honor 10
    'Mozilla/5.0 (Linux; Android 10; COL-TL10 Build/HUAWEICOL-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.145 Mobile Safari/537.36',
    # OPPO Reno2 Z Dual-SIM
    'Mozilla/5.0 (Linux; Android 10; CPH1951) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36',
    # Huawei Nova 7 Pro w/ HuaweiBrowser
    'Mozilla/5.0 (Linux; Android 10; HarmonyOS; JER-AN10; HMSCore 5.3.0.312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 HuaweiBrowser/11.1.2.301 Mobile Safari/537.36',
    # Redmi K40
    'Mozilla/5.0 (Linux; Android 11; M2012K11AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.09.4.5079',
    # OPPO Reno5 Pro(5G)
    'Mozilla/5.0 (Linux; U; Android 11; zh-cn; PDSM00 Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.353 Mobile Safari/537.36'
    # iPhone
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/30.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/34.2 Mobile/15E148 Safari/605.1.15',
]


def read_config(filename: str) -> Tuple[str, str, str]:
    try:
        logger.info("Reading config from %s", filename)
        o = open(filename, 'r', encoding='utf-8')
        c = yaml.load(o, Loader=yaml.SafeLoader)
        ret = {
            "gpsjd": float(c["gpsjd"]),
            "gpswd": float(c["gpswd"]),
            "kzl34": {},
        }
        restricted_keys = ["jzdz","kzl1","kzl2","kzl3","kzl4","kzl5","kzl6","kzl7","kzl8","kzl9","kzl10","kzl11","kzl12","kzl13","kzl14","kzl15","kzl16","kzl17","kzl18","kzl19","kzl20","kzl21","kzl22","kzl23","kzl24","kzl25","kzl26","kzl27","kzl28","kzl29","kzl30","kzl31","kzl32","kzl33"]
        for k in restricted_keys:
            ret[k] = str(c[k])
        if "kzl38" not in c:
            ret["kzl38"] = ret["kzl6"]
            ret["kzl39"] = ret["kzl7"]
            ret["kzl40"] = ret["kzl8"]
        else:
            ret["kzl38"] = str(c["kzl38"])
            ret["kzl39"] = str(c["kzl39"])
            ret["kzl40"] = str(c["kzl40"])
        ret = (c['username'], c['password'], ret)
        return ret
    except OSError:
        logger.error('Fail to read configuration from %s', filename)
    except yaml.YAMLError:
        logger.error('Fail to parse YAML')
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog='yqxx', description='Auto submitter for xg.hit.edu.cn yqxx')
    parser.add_argument('-c', '--conf-file',
                        help='Set config file path',
                        required=True)
    parser.add_argument('-d', '--debug',
                        help='Set debug mode on',
                        action='store_true')
    parser.add_argument('-f', '--force',
                        help='Override previous yqxx if available',
                        action='store_true')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    (username, password, data) = read_config(args.conf_file)
    logger.info('Logging in to xg.hit.edu.cn')
    try:
        s = idslogin(username, password)
    except Exception as e:
        logger.error('Failed while logging in')
        logger.error(e)
        sys.exit(1)
    import hashlib
    h = hashlib.sha1(username.encode())
    ua = USER_AGENT_LIST[int(h.hexdigest(), 16) % len(USER_AGENT_LIST)]
    logger.info('''Using '%s' as User-Agent''' % ua)
    s.headers.update({
        'User-Agent': ua
    })
    s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange', headers={
        'Referer': 'https://xg.hit.edu.cn/'
    })
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common', headers={
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange'
    })
    _ = urllib.parse.urlparse(r.url)
    if _.hostname != 'xg.hit.edu.cn':
        logger.error('Login failed')
        sys.exit(1)
    logger.info('Login success')

    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getZnx', headers={
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
    })
    r.encoding = r.apparent_encoding
    j = json.loads(r.text)
    Znx = len(j['module'])
    data = {
        'info': json.dumps({
            "model": data
        })
    }
    logger.debug("data: %s", data['info'])
    r = s.post(
        'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/save', data=data, headers={
            'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew'
        })
    logger.debug(r.text)
    j = json.loads(r.text)
    logger.debug(j)
    if j['isSuccess']:
        logger.info("save: Success")
    else:
        logger.error("save: Failed")
        exit(1)
    if Znx != 0:
        logger.error('您有未阅读的消息，请尽快阅读。')
        exit(1)
    return


if __name__ == "__main__":
    main()
