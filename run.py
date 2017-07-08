import tweepy, random
import markovgen
from time import sleep
import boooootttt as bot

bot_ = bot.bot()
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)
while True:
    text = markov.generate_markov_text()
    bot_.do_tweet(text)
    rando = random.randint(3600,10800)
    sleep(rando)
