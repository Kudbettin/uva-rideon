from drives.models import Drive

def filter_cost_low(value, query):
	return query
def filter_cost_mid(value, query):
	return query
def filter_cost_high(value, query):
	return query
def filter_cost_extreme(value, query):
	return query
def filter_gender_male(value, query):
	return query
def filter_gender_female(value, query):
	return query
def filter_gender_other(value, query):
	return query
def filter_driver_friend(value, query):
	return query
def filter_passegner_friend(value, query):
	return query
def filter_rating_5(value, query):
	return query
def filter_rating_4(value, query):
	return query
def filter_rating_3(value, query):
	return query
def filter_rating_2(value, query):
	return query
def filter_search_text(value, query):
	return query

def search_drives(json_data):
	query = Drive.objects.all()
	
	for key, value in json_data.items():
		if key is "cost_low":
			query = filter_cost_low(value, query)
		elif key is "cost_mid":
			query = filter_cost_mid(value, query)
		elif key is "cost_high":
			query = filter_cost_high(value, query)
		elif key is "cost_extreme":
			query = filter_cost_extreme(value, query)
		elif key is "gender_male":
			query = filter_gender_male(value, query)
		elif key is "gender_female":
			query = filter_gender_female(value, query)
		elif key is "gender_other":
			query = filter_gender_other(value, query)
		elif key is "driver_friend":
			query = filter_driver_friend(value, query)
		elif key is "passegner_friend":
			query = filter_passegner_friend(value, query)
		elif key is "rating_5":
			query = filter_rating_5(value, query)
		elif key is "rating_4":
			query = filter_rating_4(value, query)
		elif key is "rating_3":
			query = filter_rating_3(value, query)
		elif key is "rating_2":
			query = filter_rating_2(value, query)
		elif key is "search_text":
			query = filter_search_text(value, query)
		else:
			pass
			
	return query