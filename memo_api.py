#   memo_api.py
#   Tehillah Kangamba 7859367   
#   Comp3010
#   Assignment 2
#   responds with json to http requests

import uuid
import json

def make_json(memo):
    return json.dumps(memo)
    
def routes():
    pass