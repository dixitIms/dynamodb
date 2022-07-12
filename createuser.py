# from asyncio import constants
from http import client
import boto3
import os
import json


def putItems(event , context):
    print(event, ">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    city = json.loads(event['body'])
    print(city, "CITY========CITY")
    parmas = {
        'id' :  city['id'],
        'name': city['name'],
        'cityRank': city['cityRank'],
        'famousFor': city['famousFor']
    }
    try:
        print("in this TRY")
        client = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = client.Table('citiesData')
        print(table, "?????TABLE")
        res = table.put_item(Item=parmas)
        print(res, "========================RES")
        return{
            'statusCode':200,
            'body': json.dumps(res)
        }
    except Exception as error:
        return{
            'statusCode':501,
            'body': json.dumps(f'Error while User add{error}')
        }

def getItems(event , context):
    id = event['queryStringParameters']['id']
    name = event['queryStringParameters']['name']
    try:
        print("in this TRY")
        client = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = client.Table('citiesData')
        print(table, "?????TABLE")
        res = table.get_item(Key={'id':id, 'name': name}).get('Item')
        print(res, "========================RES")
        return{
            'statusCode':200,
            'body': json.dumps(res)
        }
    except Exception as error:
        print("EXCEPTION ERROR")
        return{
            'statusCode':501,
            'body': json.dumps(f'Error while User add{error}')
        }

def getAllCities(event, context):
    try:
        client = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = client.Table('citiesData')
        body = table.scan()
        items = body['Items']
        print(items, ">>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return{
            'statusCode':200,
            'body': json.dumps(items)
        }
    except Exception as error:
        return{
            'statusCode':501,
            'body': json.dumps(f'Error while User add{error}')
        }

def updateCity(event, context):
    
    city = json.loads(event['body'])
        # res = table.get_item(Key={
        #     'id': city['id'], 'name': city['name'],
        # }).get('Item')
    try:
        print('IN THIS CONDITION')
        client = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = client.Table('citiesData')
        data=table.update_item(Key={
            'id': city['id'], 'name': city['name']
        },UpdateExpression="SET #famousFor = :famousFor",
        ExpressionAttributeValues={
            ':famousFor': city['famousFor']
        },
        ExpressionAttributeNames={
            '#famousFor': "famousFor"
        },
        ReturnValues="UPDATED_NEW")
        print(data, "------>>>>>>DATAAAA")
        return{
            'statusCode':200,
            'body': json.dumps(data)
        }
    except Exception as error:
        return{
            'statusCode':501,
            'body': json.dumps(f'Error while User add{error}')
        }

def deleteCity(event, context):
    data = json.loads(event['body'])
    try:
        client = boto3.resource('dynamodb', region_name= 'us-east-1')
        table = client.Table('citiesData')
        res = table.delete_item(Key={
            'id': data['id'], 'name': data['name']
        })
            # if not res['Attributes']:
        #     raise KeyError('Item not found!')
        return{
            'statusCode':200,
        }
    except Exception as error:
        print(error, "><><><><><>")
        return{
            'statusCode':501,
            'body': (f'Error while delete {error}')
        }
