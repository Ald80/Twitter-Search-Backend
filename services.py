import re
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from config import authentication, ibm_api_key

def clean_tweet(tweet):
    text_filtred = ' '.join(re.sub("(RT.@\S+|https?://\S+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                            "", tweet).split())
    re.sub(r"[^a-zA-Z0-9]+", " ", text_filtred)
    return text_filtred

def generate_sentiment_data(tweet):
    ibm_key = ibm_api_key()
    authenticator = IAMAuthenticator(ibm_key)
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
    print(json.dumps(response))
    return response

def search_tweet(query_content):
    api = authentication()
    tweets = api.search_tweets(q=query_content, tweet_mode='extended', count=100)
    tweet_data = create_tweet_dict(tweets)
    return tweet_data

def create_tweet_dict(tweets):
    tweets_list = []

    for tweet in tweets:

        parsed_tweet = {}
        tweet_full_text = tweet.full_text
        text_cleaned = clean_tweet(tweet_full_text)
        parsed_tweet['full_text'] = tweet_full_text
        parsed_tweet['full_text_cleaned'] = text_cleaned

        if tweet.retweet_count > 0:
            if parsed_tweet not in tweets_list:
                tweets_list.append(parsed_tweet)
        else:
            tweets_list.append(parsed_tweet)
            
        return tweets_list

# if __name__=="__main__":
    # tweet = '''
    # Os EUA tocaram fogo na Ucrânia, provocando uma recessão na UE, e agora ficam jogando gasolina em Taiwan, para provocar a China. 
    # Isso tudo apoiado pela indústria de armas que já está faturando horrores com a guerra na Ucrânia!
    # '''
    # result = generate_sentiment_data(tweet)
    # result = {"usage": {"text_units": 1, "text_characters": 240, "features": 1}, "sentiment": {"document": {"score": -0.785047, "label": "negative"}}, "language": "pt"}
    # sentiment_data = result['sentiment']['document']
    # print(result['sentiment']['document'])
    # print(sentiment_data['score'])
    # print(sentiment_data['label'])