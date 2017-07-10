#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import config
import boooootttt as bot

#Twitter API credential



def get_all_tweets(screen_name):
	with open('database.txt','w') as outfile:
		outfile.write('')
	database = []

	bot_ = bot.bot()
	api = bot_.api

	#Twitter only allows access to a users most recent 3240 tweets with this method

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print("...%s tweets downloaded so far" % (len(alltweets)))

		with open('database.txt','a') as outfile:
			for tweet in alltweets:
				if 'RT' in tweet.text:
					pass
				else:
					outfile.write(tweet.text)
