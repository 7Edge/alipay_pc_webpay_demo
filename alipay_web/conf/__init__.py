#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: __init__.py
# Date: 4/10/2019

"""
配置文件
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

# 中间件
##
allow_sites = ['http://127.0.0.1:8080', 'http://localhost:8080']

# 支付宝
# 这里我自己的账号绑定的支付宝沙箱环境

appid = '2016092200572114'
alipay_gateway = 'https://openapi.alipaydev.com/gateway.do'
ali_pub_key_path = os.path.join(BASE_DIR, '/keys/支付宝沙箱公钥2048.txt')
app_private_key_path = os.path.join(BASE_DIR, '/keys/应用私钥2048.txt')

if __name__ == '__main__':
    pass
