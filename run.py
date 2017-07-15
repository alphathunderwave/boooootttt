"""import functions to use"""

import tweepy, random
from apscheduler.schedulers.blocking import BlockingScheduler
import markovgen
import time
import boooootttt as bot


"""creates a new instance of boooootttt"""

bot_ = bot.bot()

"""creates a new instance of Markov and uses database.txt as an infile."""

with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)

"""calls generate_markov_text and sends that to the bot to tweet out.
	the BlockingScheduler schedules run_tweet as a job and runs it every 1-3
	hours"""
	
def run_tweet():
	try:
		text = markov.generate_markov_text()
		bot_.do_tweet(text)
	except tweepy.TweepError as e:
		print(e)

rando = random.randint(3600,10800)
scheduler = BlockingScheduler()
scheduler.add_job(run_tweet,'interval', minutes = rando)
scheduler.start()
