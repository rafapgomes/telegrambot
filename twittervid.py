import ttkeys
import tweepy
import json
autenticacao = tweepy.OAuthHandler('1jPRRn1vwAbWust2acpvz4bJF','uDOuGbws7R4gJgOf5txQnsuFOlOjFjLhTi6Pvz1immfQq19Te8')

autenticacao.set_access_token('1371708586926219266-m1m9qf5EJlQHfONDOp4LTac9wgKYM1','LNuZhrm7E7FHO31p9PkrAXUIMHCMrFVKthbAhJ6FseJWp')

twitter = tweepy.API(autenticacao)


def spliturl(url):
    return url.split('/',5)[5]

def getvideourl(id):
    tweet = twitter.get_status(id,tweet_mode="extended")
    for i in tweet.extended_entities['media'][0]['video_info']['variants']:
       if i['content_type'] == 'video/mp4':
                return i



        


