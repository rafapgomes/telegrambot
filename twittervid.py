import ttkeys
import tweepy
import json
autenticacao = tweepy.OAuthHandler(ttkeys.consumer_key,ttkeys.consumer_secret)

autenticacao.set_access_token(ttkeys.access_token,ttkeys.access_token_secret)

twitter = tweepy.API(autenticacao)


def spliturl(url):
    return url.split('/',5)[5]

def getvideourl(id):
    tweet = twitter.get_status(id,tweet_mode="extended")
    return (tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'])