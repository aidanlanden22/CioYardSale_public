from pyspark import SparkContext
import itertools
import MySQLdb
import time

def create_pairs(user, items):
	item_pairs = list(itertools.combinations(items, 2))
	all_pairs = []
	for item in item_pairs:
		all_pairs.append((user, item))
	return all_pairs

db = MySQLdb.connect(host='db', user='www', passwd='$3cureUS', db='cs4501')
cursor = db.cursor()

while True:

	cursor.execute('delete from commodity_recommendation')

	sc = SparkContext("spark://spark-master:7077", "PopularItems")

	data = sc.textFile("/tmp/data/data.txt", 2)

	pairs = data.map(lambda line: line.split("\t"))   			# tell each worker to split each line of it's partition

	users_and_items = pairs.groupByKey().mapValues(list)

	users_and_pairs_of_items = users_and_items.flatMap(lambda pair: create_pairs(pair[0], pair[1]))

	pairs_of_items_and_users = users_and_pairs_of_items.distinct().map(lambda pair: (pair[1], pair[0]))

	pairs_of_items_and_counts = pairs_of_items_and_users.groupByKey().mapValues(list)

	items_and_counts = pairs_of_items_and_counts.map(lambda pair: (pair[0], len(pair[1])))

	items_and_counts_above_3 = items_and_counts.filter(lambda pair: pair[1] > 2)

	output = items_and_counts_above_3.collect()                          			# bring the data back to the master node so we can print it out

	for page_id, count in output:
	    print ("pair: %s      count %d" % (page_id, int(count)))
	print ("Popular items done")

	recs_dict = {}
	for pairs, count in output:
		if count >= 3:
			try:
				if str(pairs[1]) not in recs_dict[pairs[0]] and str(pairs[0]) != str(pairs[1]):
					recs_dict[pairs[0]] += ' '+str(pairs[1])
			except KeyError as e:
				recs_dict[pairs[0]] = str(pairs[1])
			try:
				if str(pairs[0]) not in recs_dict[pairs[1]] and str(pairs[0]) != str(pairs[1]):
					recs_dict[pairs[1]] += ' '+str(pairs[0])
			except KeyError as e:
				recs_dict[pairs[1]] = str(pairs[0])

	for key, value in recs_dict.items():
	    print ("key: %d      value: %s" % (int(key), value))
	print ("dict items done")

	to_write = ''

	for key, value in recs_dict.items():
		value_encoded = value.encode('UTF-8')
		query = 'INSERT into commodity_recommendation (item_id, recommended_items) VALUES (%d, \'%s\'); ' % (int(key), value_encoded)
		cursor.execute(query)
		to_write += (key + '\t' + value_encoded + '\n')

	with open("/tmp/data/output.txt","w") as f:
		f.write(to_write)
		f.close()

	db.commit()

	sc.stop()
	time.sleep(120)
