from drives.models import Drive
from users.models import CustomUser
from django.db.models import Q
from users.views import get_rider_rating, get_driver_rating

# TODO: make it work when cost range in drive is larger than any individual cost range
def filter_cost(search):
	costs = {"cost_low" : [0, 6], "cost_mid" : [6, 10], "cost_high" : [10, 25], "cost_extreme" : [25, 100000]}
	
	costs_filtered = [key for key, value in search.items() if key in costs.keys() and value]
	
	sub_queries = []
	for cost_key in costs_filtered:
		sub_queries.append(Q(min_cost__gte=costs[cost_key][0]) & Q(max_cost__lt=costs[cost_key][1]))
		
	if len(sub_queries) == 0:
		sub_queries.append(Q(id=1) | ~Q(id=1))
		
	query = sub_queries.pop()
	for q in sub_queries:
		query = query | q
		
	return query
	
def filter_gender(search):
	query = Q(status="Listed")
	
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
	
def filter_friends(request, search):
	if not search["driver_friend"] and not search["passegner_friend"]:
		return Q(status="Listed")
		
	queries = []
	for friend in request.user.friends.all():
		if search["driver_friend"]:
			queries.append(Q(driver__id=friend.id))
		if search["passegner_friend"]:
			queries.append(Q(passengers__id=friend.id))
			
	if len(queries) == 0:
		return Q(id=-1)
			
	main_query = queries.pop()
	for query in queries:
		main_query = main_query | query
		
	return main_query
	
def filter_rating(search):
	query = Q(status="Listed")

	rating_options = {"rating_2", "rating_3", "rating_4", "rating_5"}
	ratings = [key for key, value in search.items() if key in rating_options and value]
	if len(ratings) == 0:
		return query

	# Make a base query from one of the ratings in the list
	value = int(ratings.pop().split("_")[1])
	query = Q(driver__driver_rating__gte=value)
	
	# Add the other ratings
	for rating in ratings:
		value = int(rating.split("_")[1])
		query = query | Q(driver__driver_rating__gte=value)
	
	return query
	
def filter_search(search):
	if not search.get("search_text", False):
		return Q(status="Listed")
		
	search_text = search["search_text"]
	return Q(description__icontains=search_text) | Q(title__icontains=search_text) | Q(payment_method__icontains=search_text) | Q(driver__username__icontains=search_text)

def search_drives(request, json_data):
	# Base query is for all objects
	query = Q(status="Listed")
	
	# Filter with 'AND' for each search category
	query = query & filter_cost(json_data)
	query = query & filter_gender(json_data)
	query = query & filter_friends(request, json_data)
	query = query & filter_rating(json_data)
	query = query & filter_search(json_data)
	
	return Drive.objects.filter(query)