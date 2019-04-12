#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: conf.py
# Date: 4/10/2019

"""
配置文件
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 中间件
##
allow_sites = ['http://127.0.0.1:8080', 'http://localhost:8080']

# 支付宝
# 这里我自己的账号绑定的支付宝沙箱环境

appid = '2016092200572114'
alipay_gateway = 'https://openapi.alipaydev.com/gateway.do'
ali_pub_key_path = os.path.join(os.path.join(BASE_DIR, 'secret_key'), '支付宝沙箱公钥.txt')  # 支付宝公钥，用于验签
app_private_key_path = os.path.join(os.path.join(BASE_DIR, 'secret_key'), '应用私钥2048.txt')  # 用户私钥，用于签名
callback_pre_url = 'http://127.0.0.1:8000'  # 注意拼接时的/杠有没有多加

if __name__ == '__main__':
    print(ali_pub_key_path, app_private_key_path)
