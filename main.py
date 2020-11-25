import base64
import logging
import random
import re
import urllib

import requests
from bs4 import BeautifulSoup
from utils import rds, encrypt
from config import *
logging.basicConfig(level=logging.INFO)




def main():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36'
    })
    # Login via ids.hit.edu.cn
    r = s.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/common')
    logging.info(r.status_code)
    pwd_default_encrypt_salt = re.compile(
        'pwdDefaultEncryptSalt = "(.*)"').search(r.text).groups()[0]
    logging.info('pwdDefaultEncryptSalt: %s' % pwd_default_encrypt_salt)
    passwordEncrypt = encrypt(
        rds(64).encode()+password.encode(), pwd_default_encrypt_salt.encode())
    logging.info(passwordEncrypt.decode())
    soup = BeautifulSoup(r.text, 'html.parser')
    # Detect Captcha
    _ = s.get("http://ids.hit.edu.cn/authserver/needCaptcha.html?username=%s&pwdEncrypt2=pwdEncryptSalt" % username)
    if _.text == "true":
        logging.error("Need Captcha")
        exit(1)
    logging.info("No captcha is needed")
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
    logging.info(r.status_code)
    logging.info(r.text)


if __name__ == "__main__":
    main()
