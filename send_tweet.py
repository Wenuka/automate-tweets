import tweepy
import logging
import traceback
import pandas as pd


def send_tweet(tweet_array):
    """
    script for sending threaded tweets on Twitter, with automatic character 
    limit checks and numbering for each tweet, simplifying the process of 
    sharing tweetstorms or series of related tweets.
    input: tweet_array; a list of list containing each tweets content.
    return: None
    """
    # twitter API v2 client
    twitter_auth_keys = {
        "api_key"        : "your_api_key",
        "api_key_secret"     : "your_api_key_secret",
        "access_token"        : "your_access_token",
        "access_token_secret" : "your_access_token_secret",
    }
    client = tweepy.Client(consumer_key=twitter_auth_keys['api_key'],
                       consumer_secret=twitter_auth_keys['api_key_secret'],
                       access_token=twitter_auth_keys['access_token'],
                       access_token_secret=twitter_auth_keys['access_token_secret'])
    tweet_count = len(tweet_array)
    # add numberig if there are more than one tweet
    processed_tweets = []
    for i in range(tweet_count):
        tweet = f"({i+1}/{tweet_count}) " if tweet_count > 1 else ""
        tweet += "\n".join(tweet_array[i])
        processed_tweets.append(tweet)
        assert len(tweet) < 281, f"atleast one tweet is more than the limit ({len(tweet)})"
    in_reply_to_tweet_id = None
    for tweet in processed_tweets:
        response = client.create_tweet(text=tweet, in_reply_to_tweet_id=in_reply_to_tweet_id)
        in_reply_to_tweet_id = response.data["id"]


def quotes_tweet(quote, author, author_short):
    """
    creates the content of the tweet.
    change this as necessary
    """
    tweet_array = [f"✨ Start your day with a dose of positivity! ✨\n"]
    tweet_array.append(f"{quote} - {author}")
    new_txt = f"\n#Happiness #PositiveVibes #DailyInspiration #{author_short.title().replace(' ','').replace('.','')} #ChooseJoy"
    new_txt_len = len(new_txt)
    tweet_array.append(new_txt)
    return tweet_array


def post_pred_to_tweet():
    """
    function to read the csv file, select a quote, process it and send it.
    """
    quotes_csv = "daily_quotes.csv" # file to store all quotes
    local_id = 0
    try_count = 3
    while True:
        try:
            all_quotes = pd.read_csv(quotes_csv, index_col="id") # reads all quotes
            quote_details = all_quotes[~all_quotes.used].iloc[local_id] # select an un-used quote
            all_quotes.loc[quote_details.name, "used"] = True # change the status of the selected quote
            all_quotes.to_csv(quotes_csv)
            processed_quote = quotes_tweet(**quote_details.iloc[:3]) # pre-process the quote
            send_tweet([processed_quote]) # send the tweet
            logging.info("Tweet sent!")
            return True
        except: # handle if there is an exception
            traceback.print_exc()
            err_msg = f"Unkown error for local_id {local_id}. Trying next"
            logging.error("Tweet error: " + err_msg)
            local_id += 1
            try_count -= 1
            if try_count < 0:
                break
    return False


if __name__ == "__main__":
    post_pred_to_tweet()
