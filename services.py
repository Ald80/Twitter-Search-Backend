import re
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from config import authentication, ibm_api_key
from tweepy import TweepError

def clean_tweet(tweet) -> str:
    text_cleaned: str = ' '.join(re.sub("(RT.@\S+|https?://\S+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                            "", tweet).split())
    text_cleaned = remove_special_characters(text_cleaned)    
    return text_cleaned

def remove_special_characters(text: str):
    text_filtred: str = re.sub(r'(\\u[0-9A-Fa-f]+)', lambda match_text: chr(int(match_text.group(0)[2:] , 16)), text)
    return text_filtred

def extract_sentimen_data(sentiment_dict: dict) -> dict:
        dict_parsed: dict = {}
        if type(sentiment_dict) == dict:
            dict_parsed = sentiment_dict['sentiment']['document']
        return dict_parsed

def generate_sentiment_data(tweet):
    try:
        ibm_key = ibm_api_key()
        authenticator = IAMAuthenticator(apikey=ibm_key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        url_service = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7819a45e-92a1-4e45-be50-dd80c3fe51de"
        natural_language_understanding.set_service_url(url_service)
        response = natural_language_understanding.analyze(
            text=tweet,
            features=Features(sentiment=SentimentOptions(document=True))
        ).get_result()
        return response
    except ApiException as e:
        print(e.message)

def search_tweet(query_content: str):
    tweets = None
    try:
        api = authentication()
        filter_retweets = "-filter:retweets"
        tweets = api.search(q=query_content+filter_retweets, tweet_mode='extended', count=100)
    except TweepError as e:
        print(e.response)
    return tweets


def list_tweet_data(tweets) -> list:
    tweets_list = []

    for tweet in tweets:

        parsed_tweet = {}
        tweet_full_text = tweet.full_text
        
        text_cleaned = clean_tweet(tweet_full_text)
        # sentiment_data = generate_sentiment_data(text_cleaned)
        # sentiment_document = extract_sentimen_data(sentiment_data)

        parsed_tweet['full_text'] = tweet_full_text 
        parsed_tweet['full_text_cleaned'] = text_cleaned
        # parsed_tweet['sentiment'] = sentiment_document

        tweets_list.append(parsed_tweet)
    return tweets_list
