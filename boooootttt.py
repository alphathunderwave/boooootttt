"""import funtions to use"""

import tweepy, sys, random, datetime, config, markovify, tweetdumper
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class bot():

	"""__init__ initiates the bot, sets up consumer and access keys and secrets
	and logs into twitter.  it also creates a list for followers. config.py is
	needed to complete the login"""

	def __init__(self):
		CONSUMER_KEY = config.CONSUMER_KEY
		CONSUMER_SECRET = config.CONSUMER_SECRET
		ACCESS_KEY = config.ACCESS_KEY
		ACCESS_SECRET = config.ACCESS_SECRET
		self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		self.api = tweepy.API(self.auth, wait_on_rate_limit = True)
		#self.reddit = praw.Reddit(username = config.username,password = config.password, client_id = config.client_id, client_secret = config.client_secret, user_agent = "boooootttt test bot 0.1")
		#self.subreddit = self.reddit.subreddit('totallynotrobots')


	"""do_tweet takes in a string and submits it to twitter. the text is trimmed
	 to make sure that the tweet does not go over twitters limit of 140
	 characters"""

	def do_tweet(self):
		try:
			random_follower = self.api.followers()[random.randint(0,len(self.api.followers()))]

			with open("tweets/" + random_follower.screen_name + '_tweets.txt', 'r') as f:
				text = f.read()
			text_model = markovify.NewlineText(text)

			out = text_model.make_short_sentence(140)
			status = self.api.update_status(out[0:140])
			tid = status.id
			self.log('Tweet Sent')

		except tweepy.TweepError as e:
			self.log('Tweet Failed')
			self.log(e)


	"""reply takes in a twitter status and a string and submits the string as a
	reply to the status. like the do_tweet function, the tweet is limited to 140
	 characters"""

	def reply(self,status):
		ids = self.read_ids(status).split(' ') #this isnt working rn~~~~~~~~~~
		tid = ids[0]
		rid = ids[1]
		'''
		submission = praw.models.Submission(self.reddit,id=rid)

		for comment in submission.comments:
			#text = comment.body
			rando = random.randint(0,9)
			if rando == 5:
				break
		status = self.api.update_status(text[0:140],status)
		tid = status.id
		self.log('tweet sent')
		self.write_ids(rid,tid)'''

	"""downloads all tweeets by a user using tweetdumper"""

	def dump_tweets(self):
		for follower in self.api.followers():
			try:
				tweetdumper.get_all_tweets(follower.screen_name)
			except Exception as e:
				self.log('Dump Failed')
				self.log(e)

	"""logs the successes and failures of the bot"""

	def log(self,text):
		date_time = datetime.datetime.now()

		date = date_time.date()
		time = date_time.time()

		out = str(date.month) + '/' + str(date.day) + '/' + str(date.year) + ' at ' + str(time.hour) + ':' + str(time.minute) + ' ' + str(text) + '\n'
		with open('log.txt','a') as outfile:
			outfile.write(out)

		print(out)
