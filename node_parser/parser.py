import os

from dotenv import load_dotenv
from icecream import ic
from solana.rpc.api import Client

load_dotenv()


def connect_client():
    client = Client(os.environ["NODE_URL"])
    if client.is_connected():
        return client
    raise Exception("failed to connect")


def get_current_slot(client):
    epoch = client.get_epoch_info()
    ic(epoch)
    return epoch['result']['absoluteSlot']


def get_blocks(client, start, end=None):
    blocks = client.get_confirmed_blocks(start, end)
    ic(blocks)
    return blocks["result"]


def get_block(client, slot):
    block = client.get_confirmed_block(slot)
    ic(block)


if __name__ == '__main__':
    client = connect_client()
    slot = get_current_slot(client)
    blocks = get_blocks(client, slot-1, slot)
    for b in blocks:
        get_block(client, slot)
