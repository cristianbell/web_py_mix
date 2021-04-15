# -*- coding: iso-8859-1 -*-
import time
import os
from datetime import datetime

import redis
from flask import Flask, request, Response
from pycognito import Cognito
import boto3
import botocore.exceptions
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
import json
# import requests

import env

token = ''
expiresIn = 0
headers = {
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    # 'Authorization': env.api_key,
    'Content-Type': 'application/json'
}
login_data = {}
#sess = requests.Session()
sess = None

os.environ['AWS_DEFAULT_REGION'] = env.REGION

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            val = cache.incrbyfloat('hits', 0.2)
            cache.set('hits', val)
            return val
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    # connect to cognito
    global token, sess, expiresIn, headers

    REGION = env.REGION
    USER_POOL_ID = env.USER_POOL_ID
    CLIENT_ID = env.CLIENT_ID
    CLIENT_SECRET = env.CLIENT_SECRET
    ACCESS_ID = env.ACCESS_ID
    ACCESS_KEY = env.ACCESS_KEY

    u_username = 'testerus'
    u_password = 'passW0rd'
    u_mail = 'mail@mail.com'

    out_txt = ''

    headers['Authorization'] = 'Bearer {}'.format(env.api_key)
    # u = Cognito(env.REGION, env.CLIENT_ID, client_secret=env.CLIENT_SECRET)
    # user = u.get_users(attr_map={"given_name": "first_name", "family_name": "last_name"})

    client = boto3.client('cognito-idp', region_name=REGION, aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)

    def get_secret_hash(username):
        msg = username + CLIENT_ID
        dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def sign_up():
        global out_txt
        try:
            # Add user to pool
            sign_up_response = client.sign_up(
                ClientId=CLIENT_ID,
                Username=u_username,
                Password=u_password,
                UserAttributes=[{'Name': 'email',
                                 'Value': u_mail}])
            out_txt += '{}\n<br/>'.format(sign_up_response)
            out_txt += "    Confirming user...\n<br/>"
            # Use Admin powers to confirm user. Normally the user would
            # have to provide a code or click a link received by email
            confirm_sign_up_response = client.admin_confirm_sign_up(
                UserPoolId=USER_POOL_ID,
                Username=username)
            out_txt += '{}\n<br/>'.format(confirm_sign_up_response)
        except ClientError as err:
            # Probably user already exists
            out_txt += '{}\n<br/>'.format(err)

    def get_users():
        response = client.list_users(
            UserPoolId=USER_POOL_ID,
            AttributesToGet=[
                'string',
            ],
            Limit=50,
            PaginationToken='string',
            Filter='string'
        )

    sign_up(out_txt)


    #r = sess.post(env.url_auth, headers=headers)
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. {}\n{}'.format(count, out_txt, headers)
    # login, get_companies, get_companies_proj

'''
[default]
aws_access_key_id=XXXXXXXXXXXXXX
aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYY
'''
