from mylib.logic import get_headlines
import os
import praw

reddit_read_only = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_CLIENT_USER_AGENT"),
)

def test_get_headlines():
    assert len(get_headlines("soccer")) == 3