#!/bin/usr/env python

import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
from pprint import pprint
import altair as alt
import praw
from altair_saver import save

reddit_read_only = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_CLIENT_USER_AGENT"),
)

def nltk_req():
    """Download the nltk requirements."""
    nltk.download("vader_lexicon")


def get_headlines(subred):
    """Get headlines from a subreddit."""
    headlines = set()
    subredditx = reddit_read_only.subreddit(subred).top(limit=3)
    for submission in subredditx:
        headlines.add(submission.title)
    return list(headlines)


def make_label(row):
    """Make a label for the sentiment"""
    if row["compound"] >= 0.2:
        return "Positive"
    elif row["compound"] <= -0.2:
        return "Negative"
    else:
        return "Neutral"


def get_sentiment(subred):
    """Get sentiment from a subreddit."""
    sia = SIA()
    headlines = set()
    results = []
    for submission in reddit_read_only.subreddit(subred).new(limit=None):
        headlines.add(submission.title)
    for item in headlines:
        pol_score = sia.polarity_scores(item)
        pol_score["headline"] = item
        results.append(pol_score)
    final_df = pd.DataFrame.from_records(results)
    final_df.drop(["neg", "neu", "pos"], axis=1, inplace=True)
    final_df["label"] = final_df.apply(make_label, axis=1)
    final_df.drop(["compound"], axis=1, inplace=True)
    truly_final = final_df.to_dict('records')
    return truly_final[:15]

def export_to_csv(subred):
    """Export the sentiment to a csv file."""
    sia = SIA()
    headlines = set()
    results = []
    for submission in reddit_read_only.subreddit(subred).new(limit=None):
        headlines.add(submission.title)
    for item in headlines:
        pol_score = sia.polarity_scores(item)
        pol_score["headline"] = item
        results.append(pol_score)
    final_df = pd.DataFrame.from_records(results)
    final_df.drop(["neg", "neu", "pos"], axis=1, inplace=True)
    final_df = final_df.sort_values("compound", ascending=False)
    final_df["label"] = final_df.apply(make_label, axis=1)
    final_df.drop(["compound"], axis=1, inplace=True)
    final_df.to_csv(f"{subred}.csv", index=False)

    print(f"CSV file saved to {os.getcwd()} with filename {subred}.csv")


def chk_pos_words(file_name):
    """Check the positive sentiment from a csv file."""
    df = pd.read_csv(file_name)
    print(f"These are the top 10 positive headlines from {file_name}")
    pprint(list(df[df["label"] == "Positive"].headline)[:10], width=200)


def chk_pos_words_f_api(subred):
    sia = SIA()
    headlines = set()
    results = []
    for submission in reddit_read_only.subreddit(subred).new(limit=None):
        headlines.add(submission.title)
    for item in headlines:
        pol_score = sia.polarity_scores(item)
        pol_score["headline"] = item
        results.append(pol_score)
    final_df = pd.DataFrame.from_records(results)
    final_df.drop(["neg", "neu", "pos"], axis=1, inplace=True)
    final_df = final_df.sort_values("compound", ascending=False)
    truly_final = final_df.to_dict('records')
    return truly_final[:11]

def chk_neg_words(file_name):
    """Check the positive sentiment from a csv file."""
    df = pd.read_csv(file_name)
    print(f"These are the top 10 negative headlines from {file_name}")
    pprint(list(df[df["label"] == "Negative"].headline)[-11:], width=200)

def chk_neg_words_f_api(subred):
    sia = SIA()
    headlines = set()
    results = []
    for submission in reddit_read_only.subreddit(subred).new(limit=None):
        headlines.add(submission.title)
    for item in headlines:
        pol_score = sia.polarity_scores(item)
        pol_score["headline"] = item
        results.append(pol_score)
    final_df = pd.DataFrame.from_records(results)
    final_df.drop(["neg", "neu", "pos"], axis=1, inplace=True)
    final_df = final_df.sort_values("compound", ascending=True)
    truly_final = final_df.to_dict('records')
    return truly_final[:11]

# check how many positive and negative headlines there are
def chk_pos_neg_words(subred):
    sia = SIA()
    headlines = set()
    results = []
    for submission in reddit_read_only.subreddit(subred).new(limit=None):
        headlines.add(submission.title)
    for item in headlines:
        pol_score = sia.polarity_scores(item)
        pol_score["headline"] = item
        results.append(pol_score)
    final_df = pd.DataFrame.from_records(results)
    final_df.drop(["neg", "neu", "pos"], axis=1, inplace=True)
    final_df["label"] = final_df.apply(make_label, axis=1)
    final_df.drop(["compound"], axis=1, inplace=True)
    final_df = final_df.label.value_counts(normalize=True).rename_axis('Label').reset_index(name='Percentage')
    final_df['Percentage'] = final_df['Percentage'] * 100
    truly_final = final_df.to_dict('records')
    return truly_final

def sum_graph(file_name):
    final_df = pd.read_csv(f'{file_name}.csv')
    final_df = (
        final_df.label.value_counts(normalize=True)
        .rename_axis("Label")
        .reset_index(name="Percentage")
    )
    final_df["Percentage"] = final_df["Percentage"] * 100
    graph = (
        (
            alt.Chart(final_df, title="Sentiment Statistics")
            .mark_bar(size=100, color="Black", opacity=0.9)
            .encode(
                x=alt.X("Label", scale=alt.Scale(zero=False), title="Sentiment"),
                y=alt.Y(
                    "Percentage",
                    scale=alt.Scale(zero=False),
                    title="Percentage",
                ),
                tooltip=["Percentage"],
            )
        )
        .properties(width=400)
    )
    return save(graph, f"{file_name}.png")