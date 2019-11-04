from drives.models import Drive
from django.db.models import Q

def filter_cost(search):
	costs = {"cost_low" : [0, 6], "cost_mid" : [6, 10], "cost_high" : [10, 25], "cost_extreme" : [25, 100000]}
	
	costs_filtered = [key for key, value in search.items() if key in costs.keys() and value]
	#costs_filtered = set(costs.keys()).intersection(set(search.keys()))
	
	sub_queries = []
	for cost_key in costs_filtered:
		print(cost_key)
		print(costs[cost_key])
		sub_queries.append(Q(min_cost__gte=costs[cost_key][0]) & Q(max_cost__lt=costs[cost_key][1]))
		
	if len(sub_queries) == 0:
		sub_queries.append(Q(id=1) | ~Q(id=1))
		
	query = sub_queries.pop()
	for q in sub_queries:
		query = query | q
		
	return query
	
def filter_gender(search):
	return Q(id=1) | ~Q(id=1)
def filter_friends(search):
	return Q(id=1) | ~Q(id=1)
def filter_rating(search):
	return Q(id=1) | ~Q(id=1)
def filter_search(search):
	return Q(id=1) | ~Q(id=1)

def search_drives(json_data):
	# Base query is for all objects
	query = Q(id=1) | ~Q(id=1)
	
	# Filter with 'AND' for each search category
	query = query & filter_cost(json_data)
	query = query & filter_gender(json_data)
	query = query & filter_friends(json_data)
	query = query & filter_rating(json_data)
	query = query & filter_search(json_data)
	
	return Drive.objects.filter(query)