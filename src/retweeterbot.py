from __future__ import absolute_import, print_function
import os
import sys
import json
import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


# Load up the twitter authentication information from the 'secret.py' file
# if the user forgot to make when, then let them know and exist.
try:
    from secret import *
except ImportError:
    print("You forgot to take the \"secret_example.py\" file, and rename it to \"secret.py\". Please do that before running this script. Also be sure that you fill the file in with your twitter credentials.")
    sys.exit(-1)


class ListenerAndRetweeter(StreamListener):
    ''' Handles data received from the stream and retweeting the specific hashtags. '''

    def __init__(self, api=None):
        # Load up the authenticated API.
        if api is None:
            print ("Streamer Error: No Api loaded.")
            sys.exit(-1)
        self.api = api or API()
            
        # Load up the bad words to avoid
        bad_words = []
        with open('bad_words.json') as data_file:
            bad_words_data = json.load(data_file)
            for website in bad_words_data['keywords']:
                bad_word = website['word']
                bad_words.append(bad_word)
        self.bad_words = bad_words

    def process_tweet(self, json_arr):
        #print(json_arr) # Debugging purposes only!
        
        # Take the ID of the tweet and re-tweet it only if you haven't
        # re-tweeted it before.
        if 'id' in json_arr.keys():
            tweet_id = int(json_arr['id'])
            tweet_text = json_arr['text']
            tweet_user = json_arr['user']

            # Verify if the tweet doesn't contain any contraversial or illegal stuff
            tweet_text = tweet_text.lower()
            is_tweet_ok = True
            for bad_word in self.bad_words:
                if bad_word in tweet_text:
                    is_tweet_ok = False

            # Verify that the tweet doesn't come from this accounts block list.
            for blocked_id in self.api.blocks_ids():
                if tweet_user['id'] == blocked_id:
                    is_tweet_ok = False

            # Do not retweet the tweet that was made by our bot!
            if tweet_user['name'] not in TWITTER_SCREEN_NAME:
                if is_tweet_ok: # Tweet is not "bad".
                    try:
                        print("Going to retweet", tweet_id)
                        self.api.retweet(tweet_id)
                    except Exception as e:
                        pass # Do nothing essentially

    def on_data(self, json_string):
        json_arr  = json.loads(json_string)
        self.process_tweet(json_arr)
        return True # To continue listening
    
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
    
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening


def mainloop():
    """ Entry point into the application """
    
    # Authenticate OAuth
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    # Setup our API.
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if not api:
        print ("Can't authenticate")
        sys.exit(-1)
    
    # Run the streamer.
    stream = Stream(auth = api.auth, listener=ListenerAndRetweeter(api))
    stream.filter(track=HASHTAGS)


if __name__ == '__main__':
    os.system('clear;')  # Clear the console text.
    
    # Keep running the Twitter Bot even with exceptions occuring until a
    # keyboard interrupt exception was detected.
    while True:
        try:
            mainloop()
        except KeyboardInterrupt:
            quit() # Stop application and quit.
        except Exception as e:
            time.sleep(1000) # Wait for a bit on error before restarting to Twitter.