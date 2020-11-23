# -*- coding: utf-8 -*-
"""
@author: Omar

"""

import tweepy, re
from textblob import TextBlob
import matplotlib.pyplot as plt

def clean_tweets(tweet):
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def percentage(part, whole):
    return format(part / whole * 100, '.2f')

def twitterSA(keyword, no_tweets):
    
    # Twitter Auth
    consumer_key = '' # Put your own consumer_key
    consumer_secret = '' # Put your own consumer_secret
    access_token = '' # Put your own access_token
    access_token_Secret = '' # Put your own access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_Secret)
    api = tweepy.API(auth)
    
    polarity = 0
    negative = 0
    neutral = 0
    positive = 0
    
    # Fetching tweets 
    tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(no_tweets)

    for tweet in tweets:
        
        analysis = TextBlob(tweet.text)
        # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average
        
        if analysis.sentiment.polarity < 0:
            negative += 1
        elif analysis.sentiment.polarity == 0:
            neutral += 1
        elif analysis.sentiment.polarity > 0:
            positive += 1
        
    print(f"After analyzing {no_tweets} tweets about {keyword} we found that the overall analysis of the tweets are: \n")
    print(f"Negative percentage: {percentage(negative, no_tweets)} %")
    print(f"Neutral percentage: {percentage(neutral, no_tweets)} %")
    print(f"Positive percentage: {percentage(positive, no_tweets)} %")
    
    # Pie Chart 
    labels = ['Negative [' + str(percentage(negative, no_tweets)) + '%]', 'Neutral [' + str(percentage(neutral, no_tweets)) + '%]', 'Positive [' + str(percentage(positive, no_tweets)) + '%]']
    sizes = [negative, neutral, positive]
    colors = ['#F54F52', '#378AFF', '#93F03B']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title(f'How people are reacting on {keyword} by analyzing {no_tweets} tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

twitterSA('love', 200)
