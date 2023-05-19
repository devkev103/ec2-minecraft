#!/usr/bin/env python3.7
# https://github.com/dejonghe/extend_cfn_example/blob/master/lambda/attach_hosted_zone/lambda_function.py
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-lambda-function-code-cfnresponsemodule.html
# if you have used my cloudwatch script to create your minecraft resources this will make the routetable we created the main route table!
import json
import boto3
import urllib
import logging
import argparse
import requests

SUCCESS = "SUCCESS"
FAILED = "FAILED"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch) 

def lambda_handler(event, context):
    try:
        logger.info("Received event: " + json.dumps(event))
        vpc_id = event['ResourceProperties']['VpcId']
        region = event['ResourceProperties']['Region']
        responseData = {}
        responseStatus = 'SUCCESS'

        if event['RequestType'] == 'Create':
            client = boto3.client('ec2', region_name=region)

            # gets all route tables associated with vpc
            response = client.describe_route_tables(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpc_id,
                        ]
                    }
                ])

            # finds the main route table assoication id and secondary route table ... this code is very basic and meant to be so. this isn't suppose to be "solid"
            for table in response['RouteTables']:
                if len(table['Associations']) > 0:
                    currentAssociationId = table['Associations'][0]['RouteTableAssociationId']
                else:
                    newRouteTable = table['RouteTableId']

            # makes the secondary route table, main route table
            response = client.replace_route_table_association(AssociationId=currentAssociationId, RouteTableId=newRouteTable)

        responseStatus = 'SUCCESS'
        logger.info('Successfully swapped to a different main route table!')
    except Exception as e:
        responseStatus = 'FAILURE'
        logger.error(str(e))
        
    if context:
        send(event, context, responseStatus, responseData)

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']
 
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData
 
    json_responseBody = json.dumps(responseBody)
 
    logger.info("Response body:\n" + json_responseBody)
 
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
 
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        logger.info("Status code: " + response.reason)
    except Exception as e:
        logger.error("send(..) failed executing requests.put(..): " + str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Foo')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-r', '--Region', help='The region to query', required=True)
    requiredNamed.add_argument('-v', '--VpcId', help='VPC to swap route tables', required=True)
    args = parser.parse_args()

    event = { 'RequestType': 'Create', 'ResourceProperties': { 'VpcId': args.VpcId, 'Region': args.Region } }
    lambda_handler(event, None)