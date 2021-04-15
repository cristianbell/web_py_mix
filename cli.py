# -*- coding: iso-8859-1 -*-
import time
import os
from datetime import datetime

#import redis
#from flask import Flask, request, Response
import pprint
import boto3
import botocore.exceptions
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
import json
import env

'''
journeymanTestPool
journeymanTestPoolClient

'''


pp = pprint.PrettyPrinter(indent=4)

headers = {}
debug_mode = True

out_txt = ''

headers['Authorization'] = 'Bearer {}'.format(env.api_key)
# u = Cognito(env.REGION, env.CLIENT_ID, client_secret=env.CLIENT_SECRET)
# user = u.get_users(attr_map={"given_name": "first_name", "family_name": "last_name"})

client = boto3.client('cognito-idp', region_name=env.REGION, aws_access_key_id=env.ACCESS_ID, aws_secret_access_key=env.ACCESS_KEY)


def get_secret_hash(username):
    global env
    dig = hmac.new(str(env.CLIENT_SECRET).encode('utf-8'),
                   msg=str(username + env.CLIENT_ID).encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


def sign_up():
    global out_txt, env
    try:
        # Add user to pool
        sign_up_response = client.sign_up(
            ClientId=env.CLIENT_ID,
            SecretHash=get_secret_hash(env.u_mail),
            Username=env.u_mail,
            Password=env.u_password,
            UserAttributes=[{'Name': 'email',
                             'Value': env.u_mail}])
        out_txt += '{}\n<br/>'.format(sign_up_response)
        out_txt += "    Confirming user...\n<br/>"
        # Use Admin powers to confirm user. Normally the user would
        # have to provide a code or click a link received by email
        '''
        out_txt += '{}\n<br/>'.format(confirm_sign_up_response)
        confirm_sign_up_response = client.admin_confirm_sign_up(
            UserPoolId=USER_POOL_ID,
            Username=u_mail)
        '''
    except ClientError as err:
        # Probably user already exists
        debug_out('{}\n<br/>'.format(err))


def get_users():
    response = client.list_users(
        UserPoolId=env.USER_POOL_ID,
        AttributesToGet=[
            'email'
        ],
        Limit=50
    )
    pp.pprint(response)


def debug_out(txt):
    global debug_mode
    if debug_mode:
        print('out: {}'.format(txt))


sign_up()
get_users()

