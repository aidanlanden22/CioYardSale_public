import time
import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

consumer = None
es = None

index = 0

while consumer == None or es == None:
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
	except:
		time.sleep(1)


for message in consumer:
	body = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=index, body=body)
	index = index + 1
	es.indices.refresh(index="listing_index")
