"""import funtions to use"""

import tweepy, sys, random, datetime
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config
import praw
import urllib.request



class bot():

	"""__init__ initiates the bot, sets up consumer and access keys and secrets
	and logs into twitter.  it also creates a list for followers. config.py is
	needed to complete the login"""

	def __init__(self):
		CONSUMER_KEY = config.CONSUMER_KEY
		CONSUMER_SECRET = config.CONSUMER_SECRET
		ACCESS_KEY = config.ACCESS_KEY
		ACCESS_SECRET = config.ACCESS_SECRET
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		self.api = tweepy.API(auth, wait_on_rate_limit = True)
		self.reddit = praw.Reddit(username = config.username,password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = "boooootttt test bot 0.1")
		self.subreddit = self.reddit.subreddit('totallynotrobots')


	"""do_tweet takes in a string and submits it to twitter. the text is trimmed
	 to make sure that the tweet does not go over twitters limit of 140
	 characters"""

	def do_tweet(self):
		for submission in self.subreddit.hot(limit=50):
			rando = random.randint(0,20)
			title = submission.title
			if '[STICKY]' in title:
				pass
			elif '.jpg' not in submission.url:
				pass
			elif rando == 5:
				break
		print(title)
		if submission.url:
			print(submission.url)
			urllib.request.urlretrieve(submission.url, "temp.jpg")

		try:
			self.api.update_with_media('temp.jpg',status=title[0:140])
			self.log('tweet sent')
			self.write_tweet(title)
		except tweepy.TweepError as e:
			self.log(e)


	"""reply takes in a twitter status and a string and submits the string as a
	reply to the status. like the do_tweet function, the tweet is limited to 140
	 characters"""

	def reply(self,status,text):
		print('not finished')


	"""wrtite_tweet writes a sent tweet to a file for saving"""

	def write_tweet(self,text):
		with open('tweetlist.txt','a') as outfile:
			outfile.write(text)

	"""logs the successes and failures of the bot"""

	def log(self,text):
		date_time = datetime.datetime.now()

		date = date_time.date()
		time = date_time.time()

		out = str(date.month) + '/' + str(date.day) + '/' + str(date.year) + ' at ' + str(time.hour) + ':' + str(time.minute) + ' ' + str(text) + '\n'
		with open('log.txt','a') as outfile:
			outfile.write(out)

		print(out)
bot_ = bot()
bot_.do_tweet()
