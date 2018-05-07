import time
import json

from kafka import KafkaConsumer

consumer = None

while consumer == None:
    try:
        consumer = KafkaConsumer('my_recommendation', group_id='listing-recommendations', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(1)

for message in consumer:
    json_obj = json.loads((message.value).decode('utf-8'))
    with open("/data/data.txt") as output:
        output.write(json_obj['username'] + '\t' + json_obj['item'] + '\n')
        output.close()
