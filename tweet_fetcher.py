'''
   fetch tweets based on the keywords

'''
import tweepy
import html
import preprocessor
import configparser

class TweetsLimit(Exception):
    '''Custom exception raised when number of tweets is more than MAX_TWEETS'''
    def __str__(self):
        return 'No. of tweets >= MAX'


def connect():

    # Twitter app secrets
    config = configparser.ConfigParser()
    config.read('config.ini')
    consumer_key = config.get('twitterAppSecrets', 'consumer_key')
    consumer_secret = config.get('twitterAppSecrets', 'consumer_secret')
    access_token = config.get('twitterAppSecrets', 'access_token')
    access_token_secret = config.get('twitterAppSecrets', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api




def fetch(api, kword, MAX_TWEETS = 10):

    l = []
    try:
        for tweet in tweepy.Cursor(api.search,
                                q=kword,
                                count=10,
                                result_type="mixed",
                                include_entities=False,
                                lang="en").items():
            l.append(preprocessor.clean(html.unescape(tweet.text)))
            if len(l) > MAX_TWEETS:
                raise TweetsLimit
    except TweetsLimit as e:
        print('Success:', e)
    except Exception as e:
        print('Error (probably Rate Limit Exceeded Exceeded):', e)
    return l






# In below method count does not work properly, hence using cursors (SLOW)
# result = api.search(q='google', lang='en', result_type='mixed', count='100') 
# print(len(result))
# print(result[0].text)
