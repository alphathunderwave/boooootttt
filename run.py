"""import functions to use"""

import tweepy, random, os
from time import sleep
import boooootttt as bot


"""creates a new instance of boooootttt"""

bot_ = bot.bot()

randcount = random.randint(20,50)
#bot_.dump_tweets()
while True:
	sleepnum = random.randint(36000,108000)
	bot_.do_tweet()
	sleep(sleepnum)
