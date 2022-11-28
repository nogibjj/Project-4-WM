from fastapi import FastAPI
from mylib.logic import get_headlines
from mylib.logic import get_sentiment
from mylib.logic import chk_pos_words_f_api
from mylib.logic import chk_neg_words_f_api
from mylib.logic import chk_pos_neg_words
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "This api will show the sentiment of a subreddit of your choice."
    }

# create a function that will take a subreddit as an argument
@app.get("/top_three/{subred}")
async def subreddit(subred: str):
    # call the get_sentiment function from mylib.logic
    df = get_headlines(subred)
    # return the result to the user
    return {"Top Three Headlines": df}


@app.get("/sentiment/{subred}")
async def sentiment(subred: str):
    # call the get_sentiment function from mylib.logic
    df = get_sentiment(subred)
    # return the result to the user
    return {"Sentiment": df}


@app.get("/positive/{subred}")
async def positive(subred: str):
    # call the get_sentiment function from mylib.logic
    df = chk_pos_words_f_api(subred)
    # return the result to the user
    return {"Positive Sentiment": df}

@app.get("/negative/{subred}")
async def negative(subred: str):
    # call the get_sentiment function from mylib.logic
    df = chk_neg_words_f_api(subred)
    # return the result to the user
    return {"Negative Sentiment": df}

@app.get("/pos_neg/{subred}")
async def pos_neg(subred: str):
    # call the get_sentiment function from mylib.logic
    df = chk_pos_neg_words(subred)
    # return the result to the user
    return {"Positive and Negative Sentiment": df}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
