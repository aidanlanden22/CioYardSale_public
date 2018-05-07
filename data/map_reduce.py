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

	cursor.exexcute('delete from commodity_recommendation')

	sc = SparkContext("spark://spark-master:7077", "PopularItems")

	data = sc.textFile("/tmp/data/recommendations.txt", 2) 

	pairs = data.map(lambda line: line.split("\t"))
	pairs2 = pairs.groupByKey().mapValues(list)
	pairs3 = pairs2.flatMap(lambda pair: create_pairs(pair[0], pair[1]))
	pairs3 = pairs3.distinct()
	pairs4 = pairs3.map(lambda pair: (pair[1], pair[0]))
	pairs4 = pairs4.groupByKey().mapValues(list)
	pairs5 = pairs4.map(lambda pair: (pair[0], len(pair[1])))
	pairs6 = pairs5.filter(lambda pair: pair[1] > 2)
	output = pairs6.collect()

	recs_dict = {}
	for page_id, count in output:
		if count >= 3:
			try:
				if str(page_id[1]) not in recs_dict[page_id[0]] and str(page_id[0]) != str(page_id[1]): 
					recs_dict[page[0]] += ' '+str(page[1])
			except KeyError as e:
				recs_dict[page[0]] = str(page[1])
			try:
				if str(page_id[0]) not in recs_dict[page_id[1]] and str(page_id[0]) != str(page_id[1]):
					recs_dict[page_id[1]] += ' '+str(page_id[0])
			except KeyError as e:
				recs_dict[page_id[1]] = str(page_id[0])


	to_write = ''
	for key, value in recs_dict.items():
		value_encoded = value.encode('UTF-8')
		query = 'INSERT INTO commodity_recommendation (item_id, recommended_items) VALUES (%d, \'%s\');' % (int(key), value_encoded)
		cursor.execute(query)
		to_write += (key + '\t' + value_encoded + '\n')

	with open("/tmp/data/output.txt","w") as f:
		f.write(to_write)
		f.close()

	db.commit()

	sc.stop()
	time.sleep(120)


