import base64
import json
import boto3

print('Loading function')

client = boto3.client('s3')
s3_bucket = 'sol-bucket-54321'


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        payload = json.loads(payload)

        # save the block
        block = payload['result']
        block_height = block['blockHeight']
        s3_blocks_path = f'blocks/{block_height}.json'
        client.put_object(
            Body=(bytes(json.dumps(block).encode('UTF-8'))),
            Bucket=s3_bucket,
            Key=s3_blocks_path,
        )

        txs = payload['result']['transactions']
        for tx in txs:
            # save tx by signature
            tx_sig = tx['transaction']['signatures'][0]
            s3_tx_path = f'tx/{block_height}/{tx_sig}.json'
            client.put_object(
                Body=(bytes(json.dumps(tx).encode('UTF-8'))),
                Bucket=s3_bucket,
                Key=s3_tx_path,
            )

            # save tx by address
            tx_sender = tx['transaction']['message']['accountKeys'][0]
            s3_tx_sender_path = f'tx_by_addr/{block_height}/{tx_sender}.json'
            client.put_object(
                Body=(bytes(json.dumps(tx).encode('UTF-8'))),
                Bucket=s3_bucket,
                Key=s3_tx_sender_path,
            )

    return 'Successfully processed {} records.'.format(len(event['Records']))
