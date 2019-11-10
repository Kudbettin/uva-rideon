from drives.models import Drive
from django.db.models import Q

def filter_cost(search):
	costs = {"cost_low" : [0, 6], "cost_mid" : [6, 10], "cost_high" : [10, 25], "cost_extreme" : [25, 100000]}
	
	costs_filtered = [key for key, value in search.items() if key in costs.keys() and value]
	
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
	query = Q(id=1) | ~Q(id=1)
	
	# Unless filtering by male or female, return all drives
	if not search.get("gender_male", False) and not search.get("gender_female", False):
		return query

	# Treat gender_other as any gender
	if search.get("gender_other", False):
		return query
	
	male_query = Q(driver__gender='male') | Q(driver__gender='Male')
	female_query = Q(driver__gender='female') | Q(driver__gender='Female')
	
	if search.get("gender_male", False):
		query = male_query
	else:
		return female_query # gender_female is the only one selected
		
	if search.get("gender_female", False):
		query = query | female_query
		
	return query
	
def filter_friends(search):
	return Q(id=1) | ~Q(id=1)
def filter_rating(search):
	return Q(id=1) | ~Q(id=1)
def filter_search(search):
	if not search.get("search_text", False):
		return Q(id=1) | ~Q(id=1)
		
	search_text = search["search_text"]
	return Q(description__icontains=search_text) | Q(title__icontains=search_text) | Q(payment_method__icontains=search_text) | Q(driver__username__icontains=search_text)

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