import tweepy, random
import markovgen
from time import sleep

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boooootttt as bot


bot_ = bot.bot()
count = 0
dev = ['beeeeennnn_']

class StdOutListener(StreamListener):
	def on_status(self, status):
		global count
		count = count + 1
		if count == 15:
			sleep(15)

		if status.user.screen_name == 'boooootttt_':
			pass

		else:
			if status.user.screen_name in dev:
				if 'add_dev' in status.text:
					text = status.text.split(' ')
					dev.append(text[2])

				elif 'dump' in status.text:
					dump = bot_.dump()
					bot_.reply(status,str(dump))

				elif 'tweet' in status.text:
					response = markov.generate_markov_text()
					bot_.do_tweet(response)

				elif 'at' in status.text:
					text = status.text.split(' ')
					response = '@' + text[2] + ' ' + markov.generate_markov_text()
					bot_.do_tweet(response)

			else:
				response = markov.generate_markov_text()
				bot_.reply(status,str(response))

		return True

	def on_error(self, status):
		print(status)
		return False


l = StdOutListener()
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)

print('Listening')
stream = Stream(bot_.auth, l)
stream.userstream(_with='user')
