"""
Constants used in hydrawiser library
"""
GOOD_API_KEY = '0123-4567-8901-2345'
BAD_API_KEY = '1111-2222-3333-4444'

API_URL = 'https://app.hydrawise.com/api/v1'

STATUS_SCHEDULE = API_URL + '/statusschedule.php?api_key={}' \
                  .format(GOOD_API_KEY)
CUSTOMER_DETAILS = API_URL + '/customerdetails.php?api_key={}' \
                   .format(GOOD_API_KEY)
SET_ZONE = API_URL + '/setzone.php?api_key={}' \
           .format(GOOD_API_KEY)
