import argparse
import json
import logging
import sys
import urllib
from datetime import date
from typing import Tuple

import yaml
from hit.ids.login import idslogin

logger = logging.getLogger(__name__)


def read_config(filename: str) -> Tuple[str, str, str, str, str, str]:
    try:
        logger.info("Reading config from %s", filename)
        o = open(filename, 'r', encoding='utf-8')
        c = yaml.load(o, Loader=yaml.SafeLoader)
        if 'dqztm' not in c:
            c['dqztm'] = '01'
        if 'dqszdqu' not in c:
            c['dqszdqu'] = '230103'
        for k in c:
            c[k] = str(c[k])
        c['dqztm'] = c['dqztm'].zfill(2)
        ret = (c['username'], c['password'], c['brzgtw'],
               c['gnxxdz'], c['dqztm'], c['dqszdqu'])
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
    (username, password, brzgtw,
     gnxxdz, dqztm, dqszdqu) = read_config(args.conf_file)
    logger.info('Logging in to xg.hit.edu.cn')
    try:
        s = idslogin(username, password)
    except Exception as e:
        logger.error('Failed while logging in')
        logger.error(e)
        sys.exit(1)
    # s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36'
    })
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common')
    _ = urllib.parse.urlparse(r.url)
    if _.hostname != 'xg.hit.edu.cn':
        logger.error('Login failed')
        sys.exit(1)
    logger.info('Login success')
    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/csh')
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
                "brfsgktt": "0",  # 发烧、干咳、头痛现象
                "brjyyymc": "",  # 医院名称
                "brsfjy": "",  # 是否就医
                "brzdjlbz": "",  # 诊断结论备注
                "brzdjlm": "",  # 诊断结论
                "brzgtw": brzgtw,  # 体温
                "dqszd": "01",  # 01 国（境）内, 02 海外
                "dqszdqu": dqszdqu,  # 当前所在区
                "dqszdsheng": dqszdqu[:2] + '0000',  # 当前所在省
                "dqszdshi": dqszdqu[:4] + '00',  # 当前所在市/县
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
    logger.debug("data: %s", data['info'])
    r = s.post('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/saveYqxx', data=data)
    logger.debug(r.text)
    j = json.loads(r.text)
    if j['isSuccess']:
        logger.info("saveYqxx: Success")
    else:
        logger.error("saveYqxx: Failed")
        sys.exit(1)
    logger.debug(j)
    return


if __name__ == "__main__":
    main()
