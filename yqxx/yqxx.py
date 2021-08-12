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
        for k in c:
            c[k] = str(c[k])
        ret = (c['username'], c['password'], c['gnxxdz'])
        logger.debug(ret)
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
    (username, password, gnxxdz) = read_config(args.conf_file)
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
    s.get('https://xg.hit.edu.cn/')
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/'
    })
    s.post('https://xg.hit.edu.cn/mh/getRollNews')
    s.post('https://xg.hit.edu.cn/mh/getindextzgglist')
    s.post('https://xg.hit.edu.cn/mh/getindextzgglist')
    s.post('https://xg.hit.edu.cn/wz/getjyxxlist')
    s.post('https://xg.hit.edu.cn/mh/xyxw')
    s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange')
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange'
    })
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common')
    _ = urllib.parse.urlparse(r.url)
    if _.hostname != 'xg.hit.edu.cn':
        logger.error('Login failed')
        sys.exit(1)
    logger.info('Login success')
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/'
    })
    s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome')
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
    })
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getWdxx')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getKfsj')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getGrxx')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getXwtz')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getXwtz')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getZnx')
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getsftp')
    s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getZp?r=' + str(random.random()))
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getcpxx')
    # now in yqxx
    s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx'
    })
    s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome/getWdxx')
    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsb/csh')
    _ = json.loads(r.text)
    if _['isSuccess']:
        module = _['module']
        logger.info("Successfully created yqxx")
        logger.debug("yqxx id: %s", module)
    else:
        module = ''
        r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/getYqxxList')
        yqxxlist = json.loads(r.text)
        logger.debug(yqxxlist)
        if not yqxxlist['isSuccess']:
            logger.error(
                'Fail to getYqxxList, msg: %s', yqxxlist['msg'])
            sys.exit(1)
        yqxxlist = yqxxlist['module']['data']
        for i in yqxxlist:
            if i['rq'] == date.today().isoformat():
                if i['zt'] == '00':  # 未提交
                    module = i['id']
                    logger.info("Using previously created yqxx")
                    logger.debug("yqxx id: %s", module)
                elif i['zt'] == '01':  # 待辅导员审核
                    if args.force:
                        logger.info("You have already submitted yqxx")
                        module = i['id']
                        logger.info("Using previously created yqxx")
                        logger.debug("yqxx id: %s", module)
                    else:
                        logger.error("Find previously created yqxx, EXITING!")
                        sys.exit(0)
                else:  # 辅导员审核成功 当前状态不可提交！
                    logger.info("You cannot submit at this time!")
                    sys.exit(0)
                break
    if not module:
        logger.error('Could not find yqxx!')
        sys.exit(1)
    data = {
        'info': json.dumps({
            "model": {
                "id": module,
                "brfsgktt": "0",  # 是否有发烧、干咳、头痛等症状？
                "brsfgl": "0",  # 本人是否处于隔离期？
                "brsfjy": "0",  # 是否就医
                "brsflt": "0",  # 本人是否被社区、疾控中心等部门流调？
                "brsfmqjc": "0",  # 本人是否为密切接触者或二次密切接触者？
                "brsfqzbl": "0",  # 本人是否确诊病例？
                "brsfwzzbl": "0",  # 本人是否无症状病例？
                "brzdjlbz": "",  # 医院诊断结果
                "dqszd": "01",  # 01 国（境）内, 02 海外
                "gllx": "",  # 隔离类型
                "glyy": "",  # 隔离原因
                "glyybz": "",  # 其他原因
                "gnxxdz": gnxxdz,  # 详细地址（定位）
                "hsjcjg": "",  # 检测结果
                "hwcs": "",  # 海外城市
                "hwgj": "",  # 海外国家
                "hwxxdz": "",  # 海外详细地址
                "jrtw": "0",  # 今日体温
                "jtszdsfzgfx": "0",  # 家庭所在地是否为中高风险地区？
                "qtbgsx": "",  # 其他需要报告的事项
                "sfhsjc": "0",  # 是否核酸检测？
                "sftjwhjhb": "0",  # 14天内是否途径中高风险地区或境外返回？
                "sftzrychbwhhl": "0",  # 本人或共同居住人是否与确诊、疑似、无症状病例行程轨迹有交集？
                "sjszdsfzgfx": "0",  # 实际所在地是否为中高风险地区？
                "sjxxdz": "",  # 详细居住地
            }
        })
    }
    logger.debug("data: %s", data['info'])
    s.headers.update({
        'Referer': 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsb/editMrsb?id=%s&zt=01' % module
    })
    r = s.post(
        'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsb/saveYqxx', data=data)
    logger.debug(r.text)
    j = json.loads(r.text)
    logger.debug(j)
    if j['isSuccess']:
        logger.info("saveYqxx: Success")
    else:
        logger.error("saveYqxx: Failed")
        sys.exit(1)
    return


if __name__ == "__main__":
    main()
