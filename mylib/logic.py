#!/bin/usr/env python

import os
import pandas as pd
import fire
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
from pprint import pprint
import altair as alt
import praw
import altair_viewer

reddit_read_only = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_CLIENT_USER_AGENT"),
)

def nltk_req(self):
    """Download the nltk requirements."""
    nltk.download("vader_lexicon")

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
    subredditx = reddit_read_only.subreddit(subred).new(limit=None)
    for submission in subredditx:
        pol_score = sia.polarity_scores(submission.title)
        pol_score["headline"] = submission.title
        results.append(pol_score)

    # Create a dataframe
    df = pd.DataFrame.from_records(results)
    df = df.sort_values("compound", ascending=False)
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
    return df

def chk_pos_words(self, file_name):
    """Check the positive sentiment from a csv file."""
    df = pd.read_csv(file_name)
    print(f"These are the top 10 positive headlines from {file_name}")
    pprint(list(df[df["label"] == 1].headline)[:10], width=200)

def chk_neg_words(self, file_name):
    """Check the positive sentiment from a csv file."""
    df = pd.read_csv(file_name)
    print(f"These are the top 10 negative headlines from {file_name}")
    pprint(list(df[df["label"] == -1].headline)[-11:], width=200)

def sum_graph(self, file_name):
    df = pd.read_csv(file_name)
    df = (
        df.label.value_counts(normalize=True)
        .rename_axis("Label")
        .reset_index(name="Percentage")
    )
    df["Percentage"] = df["Percentage"] * 100
    graph = (
        (
            alt.Chart(df, title="Sentiment Statistics")
            .mark_bar(size=100, color="Black", opacity=0.9)
            .encode(
                x=alt.X("Label:N", scale=alt.Scale(zero=False), title="Sentiment"),
                y=alt.Y(
                    "Percentage",
                    scale=alt.Scale(zero=False),
                    title="Percentage",
                ),
                tooltip=["Percentage"],
            )
        )
        .properties(width=400)
        .interactive()
    )
    return graph.show()


# if __name__ == "__main__":
#     reddit = RedditScraper()
#     fire.Fire(reddit)
