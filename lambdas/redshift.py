import base64
import boto3
from decimal import Decimal
from datetime import datetime
from time import sleep
from string import Template
from json import dumps, loads
import logging

client = boto3.client('redshift-data')
redshift_cluster_id = "sol-redshift"
redshift_db = "dev"
redshift_user = "awsuser"
aws_region_name = "us-east-1"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def tdumps(x):
    try:
        return dumps(x)
    except:
        return x


def lambda_handler(event, context):
    n_records = len(event['Records'])
    logger.info(f'BEGIN PROCESSING {n_records} RECORDS.')

    i = 1
    for record in event['Records']:
        query_ids = []

        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        payload = loads(payload)

        # save the block
        block = payload['result']

        blockhash = block['blockhash']
        blockTime = datetime.utcfromtimestamp(block['blockTime']).strftime('%Y-%m-%d %H:%M:%S')
        blockHeight = block['blockHeight']
        parentSlot = block['parentSlot']
        previousBlockhash = block['previousBlockhash']
        rewards = tdumps(block['rewards'])

        template = Template(
            """
            insert into public.blocks values (
                '$blockhash', 
                '$blockTime', 
                $blockHeight, 
                $parentSlot,
                '$previousBlockhash',
                JSON_PARSE('{"x":$rewards}')
            );
            """
        )
        query = template.substitute(
            blockhash=blockhash,
            blockTime=blockTime,
            blockHeight=blockHeight,
            parentSlot=parentSlot,
            previousBlockhash=previousBlockhash,
            rewards=rewards
        )
        # this is needed so NULLS actually appear as NULLS, not strings
        query = query.replace("\'null\'", "NULL")

        resp = client.execute_statement(
            ClusterIdentifier=redshift_cluster_id,
            Database=redshift_db,
            DbUser=redshift_user,
            Sql=query
        )
        logger.info(f'[{i}/{n_records}] BLOCK SENT: {resp["Id"]}')
        query_ids.append(resp['Id'])

        txs = payload['result']['transactions']
        for tx in txs:
            # save tx by signature
            tx_sig = tx['transaction']['signatures'][0]
            err = tdumps(tx['meta']['err'])
            fee = tx['meta']['fee']
            innerInstructions = tdumps(tx['meta']['innerInstructions'])
            logMessages = tdumps(tx['meta']['logMessages'])
            postBalances = tdumps(tx['meta']['postBalances'])
            postTokenBalances = tdumps(tx['meta']['postTokenBalances'])
            preBalances = tdumps(tx['meta']['preBalances'])
            preTokenBalances = tdumps(tx['meta']['preTokenBalances'])
            rewards = tdumps(tx['meta']['rewards'])
            status = tdumps(tx['meta']['status'])
            accountKeys = tdumps(tx['transaction']['message']['accountKeys'])
            header = tdumps(tx['transaction']['message']['header'])
            instructions = tdumps(tx['transaction']['message']['instructions'])

            template = Template(
                """
                insert into public.tx values (
                    '$tx_sig', 
                    '$err', 
                    $fee, 
                    JSON_PARSE('{"x":$innerInstructions}'),
                    JSON_PARSE('{"x":$logMessages}'),
                    JSON_PARSE('{"x":$postBalances}'),
                    JSON_PARSE('{"x":$postTokenBalances}'),
                    JSON_PARSE('{"x":$preBalances}'),
                    JSON_PARSE('{"x":$preTokenBalances}'),
                    JSON_PARSE('{"x":$rewards}'),
                    JSON_PARSE('{"x":$status}'),
                    JSON_PARSE('{"x":$accountKeys}'),
                    JSON_PARSE('{"x":$header}'),
                    JSON_PARSE('{"x":$instructions}'),
                    '$blockhash'
                );
                """
            )
            query = template.substitute(
                tx_sig=tx_sig,
                err=err,
                fee=fee,
                innerInstructions=innerInstructions,
                logMessages=logMessages,
                postBalances=postBalances,
                postTokenBalances=postTokenBalances,
                preBalances=preBalances,
                preTokenBalances=preTokenBalances,
                rewards=rewards,
                status=status,
                accountKeys=accountKeys,
                header=header,
                instructions=instructions,
                blockhash=blockhash
            )
            # this is needed so NULLS actually appear as NULLS, not strings
            query = query.replace("\'null\'", "NULL")

            resp = client.execute_statement(
                ClusterIdentifier=redshift_cluster_id,
                Database=redshift_db,
                DbUser=redshift_user,
                Sql=query
            )
            query_ids.append(resp['Id'])

        logger.info(f'[{i}/{n_records}] TXS SENT: {query_ids[1:]}')

        # because queries are async, we need to manually check their status
        # for q_id in query_ids:
        #     while True:
        #         logger.info(f"[{i}/{n_records}] {q_id}: STATUS IS {desc['Status']}")
        #         desc = client.describe_statement(Id=q_id)
        #         if desc['Status'] == 'FINISHED':
        #             break #out of inner loop, thus resuming the outer loop
        #             logger.info(f'[{i}/{n_records}] {q_id} SUCCESSFULLY PROCESSED')
        #         elif desc['Status'] in ('FAILED', 'ABORTED'):
        #             # a single failure causes function to fail
        #             logger.error(f"{q_id}: {desc}")
        #             raise Exception(f'[{i}/{n_records}] {q_id} FAILED')

        i += 1

    return 'SUCCESS: PROCESSED {} RECORDS.'.format(len(event['Records']))
