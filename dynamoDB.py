import boto3
import pprint
import env

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=env.ACCESS_ID_DDB,
                          aws_secret_access_key=env.ACCESS_KEY_DDB,
                          region_name=env.REGION)

table = dynamodb.Table('journeymanBackend-dev-talent')

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
    break

print(data)
