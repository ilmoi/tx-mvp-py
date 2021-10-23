import boto3
from dotenv import load_dotenv
from icecream import ic

load_dotenv()

client = boto3.client('kafka')
response = client.get_bootstrap_brokers(
    ClusterArn='arn:aws:kafka:us-east-1:265784926055:cluster/sol-cluster-2/eed2ac9e-da3d-498d-8cb0-3cbe4750d393-18'
)
ic(response)