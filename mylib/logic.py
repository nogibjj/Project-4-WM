#!/bin/usr/env python

import os
import praw
import pandas as pd
import fire
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk

nltk.download("vader_lexicon")

reddit_read_only = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_CLIENT_USER_AGENT"),
)


class RedditScraper:
    def get_headlines(self, subred):
        """Get headlines from a subreddit."""
        headlines = set()
        subredditx = reddit_read_only.subreddit(subred).new(limit=3)
        for submission in subredditx:
            headlines.add(submission.title)
        return list(headlines)

    def get_sentiment(self, subred):
        """Get sentiment from a subreddit."""
        sia = SIA()
        results = []
        subredditx = reddit_read_only.subreddit(subred).new(limit=3)
        for submission in subredditx:
            pol_score = sia.polarity_scores(submission.title)
            pol_score["headline"] = submission.title
            results.append(pol_score)

        # Create a dataframe
        df = pd.DataFrame.from_records(results)
        df["label"] = 0
        df.loc[df["compound"] > 0.2, "label"] = 1
        df.loc[df["compound"] < -0.2, "label"] = -1
        df2 = df[["headline", "label"]]

        # save df2 to a csv file with the name of the subreddit and the date and time
        # df2.to_csv(f'{subred}_{pd.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False) <---- this code save with second formatting
        df2.to_csv(
            f'{subred}_{pd.datetime.now().strftime("%Y-%m-%d")}.csv', index=False
        )

        print(
            f'CSV file saved to {os.getcwd()} with filename {subred}_{pd.datetime.now().strftime("%Y-%m-%d")}.csv'
        )


if __name__ == "__main__":
    reddit = RedditScraper()
    fire.Fire(reddit)
