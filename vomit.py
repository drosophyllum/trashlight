#!/usr/bin/env python

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json 
from textblob import TextBlob
import re
#import numpy as np
#Variables that contains the user credentials to access Twitter API 
access_token = "297199576-CMR5eHYtRbz71KoJBTyNPbPCcz8CbxRMmrDGKaBi"
access_token_secret = "D4hoDLLne3mQpZW2mtyRUHqqHA5mVH9KBpFGUyaExrMai"
consumer_key = "gYT97rTu4PoaA0sUrePBy8D5N"
consumer_secret = "MCN9yypNkQbAwIzbLp02XenwaG1Xgj8kp2hChvlbQbhOW42EWZ"
from collections import defaultdict

tweetmap = defaultdict(list)

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet texua
	analysis = TextBlob(tweet)#' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))
	return analysis.sentiment.polarity
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
	try: 
		obj = json.loads(data)
		print(obj['place']['full_name'])
		print(obj['place'])
		tweetmap[obj['place']['full_name']].append(obj['text'])
		print(obj['text'])
		print('sentiment:',get_tweet_sentiment(obj['text']))
		print ""
	 	xs = sorted(map(len,tweetmap.values()))
		N=100
		print(xs[-10:])
		#print(obj)
		#print "\n\n\n\n\n"
	except:
		pass
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l1 = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream1 = Stream(auth, l1)
    #stream2 = Stream(auth, l1)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(locations=[-180,-90,180,90])
#sanfrana



    N_1,N_2 = 6,6
    x1,y1,x2,y2 = -125.0011, 24.9493, -66.9326, 49.5904
    #x1,y1 = -123.0137, 37.6040
    #x2,y2 = -122.3549, 37.8324
    #Xs = np.linspace(x1,x2,N_1+1)
    #Ys = np.linspace(y1,y2,N_2+1)
    #Xs_ = [(Xs[i], Xs[i+1]) for i in range(N_1)]
    #Ys_ = [(Ys[i], Ys[i+1]) for i in range(N_2)]
    #grid = []
    #for x1_,x2_ in Xs_:
	#for y1,y2 in Ys_:
#		grid.extend([x1,y1,x2,y2])
#    print(grid)		 
    stream1.filter(locations= [x1,y1,x2,y2]) #grid) 
	#[-123.0137, 37.6040, -122.3549, 37.8324 , -77.0909, 5.4208, -73.8778, 8.8487])
    #stream1.filter(locations=[	-123.0137, 37.6040, -122.3549, 37.8324 , -77.0909, 5.4208, -73.8778, 8.8487])
    #stream.filter(locations=[-77.0909, 5.4208, -73.8778, 8.8487])
