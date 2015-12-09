#!/usr/bin/python

import base64  # to encode the surveys
import config
import json
from limesurvey import Api

# Authentication
user = config.LIME_USER
password = config.LIME_KEY
url = config.LIME_API_URL

# Build the API
lime = Api(url, user, password)

# SET TOKEN BASE and Survey
sid = config.LIME_SID
token = config.LIME_TOKEN_BASE

data_resp = {
    'token': 'ucp95ptqe74qs32',
    '999729X44X2131111': "fabio_test_update_response"
}

resu = lime.update_response(sid, json.dumps(data_resp))

print ("END EXAMPLE UPDATE_RESPONSE")
