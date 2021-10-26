from dotenv import load_dotenv

from app.kinesis_producer import send_to_kinesis_boto3
from app.node_parser import connect_client, get_current_slot, get_blocks, get_block

load_dotenv()

if __name__ == '__main__':
    client = connect_client()
    next_slot = get_current_slot(client)
    while True:
        blocks = get_blocks(client, next_slot)
        for b in blocks[1:]:
            final_block = get_block(client, b)
            send_to_kinesis_boto3(final_block, final_block['result']['blockhash'])
        next_slot = blocks[-1]
