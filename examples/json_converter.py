import json

# todo only works if you start with a array at top level
#  otherwise use https://w3percentagecalculator.com/json-to-one-line-converter/
with open("raw_block.json", "r") as read_file:
    data = json.load(read_file)

    result = [json.dumps(record) for record in data]

    with open('nd-proceesed.json', 'w') as obj:
        for i in result:
            obj.write(i+'\n')