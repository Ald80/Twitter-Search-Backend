import json
from typing import List
from flask import request, Blueprint
from services import list_tweet_data, search_tweet

url_path = Blueprint('url_path', __name__)

@url_path.route('/twitter/get/<query>', methods=['GET'])
def get_tweets(query):

    query_text: str = query
    tweets: List = search_tweet(query_text)
    list_tweets: List = list_tweet_data(tweets)
    json_object = json.dumps(list_tweets)
    
    return json_object