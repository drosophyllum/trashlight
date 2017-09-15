#!/usr/bin/env python
from lights import makecolor,printlights
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json 
from textblob import TextBlob
import re
import numpy as np
#Variables that contains the user credentials to access Twitter API 
access_token = "297199576-CMR5eHYtRbz71KoJBTyNPbPCcz8CbxRMmrDGKaBi"
access_token_secret = "D4hoDLLne3mQpZW2mtyRUHqqHA5mVH9KBpFGUyaExrMai"
consumer_key = "gYT97rTu4PoaA0sUrePBy8D5N"
consumer_secret = "MCN9yypNkQbAwIzbLp02XenwaG1Xgj8kp2hChvlbQbhOW42EWZ"
from collections import defaultdict
import time
tweetmap = defaultdict(list)
tweetcount = defaultdict(lambda: 0)
debug = False

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet texua
	analysis = TextBlob(tweet)#' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))
	return analysis.sentiment.polarity
#This is a basic listener that just prints received tweets to stdout.
N=150
class StdOutListener(StreamListener):
    def __init__(self):
	self.clock = time.time() 
	self.ema = 0 
	self.alpha = 0.01
	self.first = True
        self.lights = np.zeros((N,3))

    def on_data(self, data):
        self.lights = self.lights*self.alpha
	try: 
		obj = json.loads(data)
		tweetcount[obj['place']['full_name']] = tweetcount[obj['place']['full_name']] + 1
	 	xs = sorted(tweetcount.items(), key = lambda x: x[1] )
		top = xs[-N:]
		workingset = set(map(lambda x: x[0] ,top))
		if obj['place']['full_name'] in workingset: 
			if self.first==False:
				diff  = time.time() - self.clock
				self.clock = time.time() 
				self.ema = self.ema*(1-self.alpha) + self.alpha*diff if self.ema> 0 else diff 
			self.first=False
			sentim = get_tweet_sentiment(obj['text'])
			if debug:
				print('diff time:',self.ema)
				print(obj['place']['full_name'])
				print(obj['place'])
				print(obj['text'])
				print('sentiment:', sentim)
				print ""
				print(top)
			top_places = map(lambda x:x[0],top)
			rank = dict(zip(top_places,range(len(top_places))))[obj['place']['full_name']]
			a = np.array([1,0,0])
			b = np.array([0,0,1])
			sentim_01 = (sentim/2 +0.5)
			self.lights[rank,:] =(1-sentim_01)*a + sentim_01*b
			#print(rank,color[0],color[1],color [2])
			printlights([ makecolor(list(self.lights[i,:])) for i in range(self.lights.shape[0])])
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
    #x1,y1,x2,y2 = -125.0011, 24.9493, -66.9326, 49.5904
    x1,y1,x2,y2 = -180,-90,180,90
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
