"""import functions to use"""

import tweepy, random
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boooootttt as bot

"""creates a new instance of bot, an incremental count and a list of developers
	(beeeeennnn_ is default)"""

bot_ = bot.bot()
count = 0

"""StdOutListener is a class that listens for replies to the bot. the on status
	function runs any time the listener 'hears' a status aimed at the bot"""

class StdOutListener(StreamListener):
	def on_status(self, status):
		try:
			"""this counter only lets the bot run 15 times, then it waits for
				15 minutes to protect overusing twitter"""
			bot_.log('Status Received')

			global count
			count = count + 1
			if count == 15:
				bot_.log('Max Tweet Reached, Restarting count')
				sleep(900)
				count =0

			"""the bot wont respond to itself"""

			if status.user.screen_name == 'boooootttt_':
				pass

			else:
				"""this is the general reply for anyone who tagged the bot"""
				bot_.reply(status)
		except tweepy.TweepError as e:
			bot_.log(e)

		return True


	"""on_error prints the error status and stops the stream. this should not
		happen. if it does something is broken and needs to be fixed"""

	def on_error(self, status):
		bot_.log(status)
		return False

"""new instance of StdOutListener and markov using database.txt as an infile.
	then a stream is set up using config from the bot_. _with = 'user' lets the
	stream know we are only looking for ourself being mentioned"""

l = StdOutListener()

bot_.log('Stream Started: Listening')
stream = Stream(bot_.auth, l)
stream.userstream(_with='user')
