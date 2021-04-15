from pycognito import Cognito
import pprint
import env

pp = pprint.PrettyPrinter(indent=4)

u = Cognito(env.USER_POOL_ID, env.CLIENT_ID, client_secret=env.CLIENT_SECRET, access_key=env.ACCESS_ID, secret_key=env.ACCESS_KEY)

users = u.get_users(attr_map={"mail":"email","given_name":"first_name", "family_name": "last_name"})
for user in users:
    print('{}'.format(user.email))