import os
import tweepy


def post_tweet(text: str) -> dict:
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Tweet posted: https://x.com/i/web/status/{tweet_id}")
    return response.data
