from dotenv import load_dotenv
import os
import tweepy

def authentication():
     load_dotenv()
     consumer_key = os.environ.get("CONSUMER_KEY")
     consumer_secret = os.environ.get("CONSUMER_SECRET")
     access_token = os.environ.get("ACCESS_TOKEN")
     access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_token, access_token_secret)
     api = tweepy.API(auth)
     return api

def ibm_api_key() -> str:
     load_dotenv()
     api_key_ibm_cloud = os.environ.get("API_KEY_IBM_CLOUD")
     return api_key_ibm_cloud or ""
