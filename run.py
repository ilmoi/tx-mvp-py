from dotenv import load_dotenv
from icecream import ic

from app.firehose_producer import send_to_firehose
from app.kinesis_producer import send_to_kinesis
from app.node_parser import connect_client, get_current_slot, get_blocks, get_block

load_dotenv()

if __name__ == '__main__':
    client = connect_client()
    next_slot = get_current_slot(client)
    while True:
        blocks = get_blocks(client, next_slot)
        for b in blocks[1:]:
            final_block = get_block(client, b)
            # ic(final_block)
            # send_to_firehose(final_block)
            send_to_kinesis(final_block)
        next_slot = blocks[-1]
        # sleep(1)
