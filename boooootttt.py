"""import funtions to use"""

import tweepy, sys, random, pathlib
import markovgen
import tweetdumper
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config

class bot():

	"""__init__ initiates the bot, sets up consumer and access keys and secrets
	and logs into twitter.  it also creates a list for followers. config.py is
	needed to complete the login"""

	def __init__(self):
		self.CONSUMER_KEY = config.CONSUMER_KEY
		self.CONSUMER_SECRET = config.CONSUMER_SECRET
		self.ACCESS_KEY = config.ACCESS_KEY
		self.ACCESS_SECRET = config.ACCESS_SECRET
		self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		self.auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
		self.api = tweepy.API(self.auth, wait_on_rate_limit = True)
		self.blacklist = []

	"""do_tweet takes in a string and submits it to twitter. the text is trimmed
	 to make sure that the tweet does not go over twitters limit of 140
	 characters"""

	def do_tweet(self,text):
		self.api.update_status(text[0:140])
		print('tweet sent')
		self.write_tweet(text)

	"""reply takes in a twitter status and a string and submits the string as a
	reply to the status. like the do_tweet function, the tweet is limited to 140
	 characters"""

	def reply(self,status,text):
		user = '@' + status.user.screen_name
		id = status.id
		try:
			self.api.update_status((user +' ' + text)[0:140],id)
			print("tweet sent to: " + user.screen_name)
			self.write_tweet(text)

		except tweepy.TweepError as e:
			print(e)

	"""dump uses tweetdumper to make a list of all the tweets for each follower.
		these tweets are written to a file named database.txt"""

	def dump(self):
		bad_followers = []
		for follower in self.api.followers():
			print(follower.screen_name)
			try:
				tweetdumper.get_all_tweets(follower.screen_name)

			except tweepy.TweepError as e:
				print(e)
				bad_followers.append(follower.screen_name)

		return bad_followers


	"""check_followers is a function that follows any new followers that the bot
	 is not already following"""

	def check_followers(self):
		print('checking for new followers')
		f = self.api.friends_ids('boooootttt_')
		friends =[]
		for friend in f:
			friends.append(self.api.get_user(friend).screen_name)
		for follower in self.api.followers():
			if follower.screen_name not in friends:
				try:
					self.api.create_friendship(follower.screen_name)
					print('now following: ' + follower.screen_name)

				except tweepy.TweepError as e :
					print(e)

	"""wrtite_tweet writes a sent tweet to a file for saving"""

	def write_tweet(self,text):
		with open('tweetlist.txt','a') as outfile:
			outfile.write(text)

	def blacklist_add(self,name):
		if name not in self.blacklist:
			blacklist.append(name)
			print(name + ' added to blacklist')

	def blacklist_remove(self,name):
		if name in blacklist:
			blacklist.pop(name):
			print(name + ' removed from blacklist')
