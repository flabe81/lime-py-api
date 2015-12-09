#!/usr/bin/python

from limesurvey import Api
import base64  # para encodear la subida de surveys
import config

# Authentication
user = config.LIME_USER
key = config.LIME_KEY
url = config.LIME_API_URL

# Build the API
lime = Api(url, user, key)

# SET TOKEN BASE and Survey
sid = config.LIME_SID
token = config.LIME_TOKEN_BASE

# GET data - token
export_res = lime.export_responses_by_token(sid, token,"ca")

# Save a in a Json file
if export_res is not None:
    decoded_string = base64.b64decode(export_res)
    with open("Output.json", "w") as text_file:
        text_file.write(decoded_string)
