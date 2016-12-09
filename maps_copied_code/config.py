#! Config settings for timetravel.py

API_KEY = 'AIzaSyDXXEjfb-6OU7nq-7Y73vK3-uydxPEQPKU'

# enable this to swap the destination and origins in the afternoon (return trip)
SWAP_IN_PM=True

# comma delimited list of origins, address format
ORIGINS = ('123 Easy St, Atlanta, GA', '1000 Beachfront Drive, Boise, ID');

# only one destination supported. Wouldn't be hard to add multiple but might reach daily API usage limits
DESTINATION = '456 Main Str, Los Angeles, CA'