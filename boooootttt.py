from __future__ import absolute_import, print_function

import tweepy, sys, random, pathlib
import markovgen
import tweetdumper
from time import sleep

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import glob
import config


class bot():
	def __init__(self):
		self.CONSUMER_KEY = config.CONSUMER_KEY
		self.CONSUMER_SECRET = config.CONSUMER_SECRET
		self.ACCESS_KEY = config.ACCESS_KEY
		self.ACCESS_SECRET = config.ACCESS_SECRET

		self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		self.auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
		self.api = tweepy.API(self.auth, wait_on_rate_limit = True)

		self.followers = []

	def do_tweet(self,text):
		self.api.update_status(text[0:140])
		print('tweet sent')

	def dump(self):
		tweet_list = []
		bad_followers = []
		fol = self.api.followers()
		for i in range(len(fol)):
			print(fol[i].screen_name)
			try:
				tweets = tweetdumper.get_all_tweets(fol[i].screen_name)
				for tweet in tweets:
					if 'RT' in tweet.text:
						pass

					else:
						tweet_list.append(tweet.text)
						tweet_list.append(' ')

			except tweepy.TweepError as e:
				print(e)
				bad_followers.append(fol[i].screen_name)
		with open('database.txt','w') as outfile:
			for tweet in tweet_list:
				outfile.write(tweet)

		return bad_followers


	def reply(self,status,text):
		user = '@' + status.user.screen_name
		id = status.id
		try:
			self.api.update_status((user +' ' + text)[0:140],id)
			print("tweet sent to: " + user.screen_name)

		except tweepy.TweepError as e:
			print(e)
