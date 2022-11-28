from fastapi import FastAPI
from mylib.logic import get_headlines
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This api will show the sentiment of a subreddit of your choice."}

# create a function that will take a subreddit as an argument
@app.get("/sr/{subred}")
async def subreddit(subred: str):
    # call the get_sentiment function from mylib.logic
    df = get_headlines(subred)
    # return the result to the user
    return {"data":df}

@app.get("/add/{num1}/{num2}")
async def add(num1: int, num2: int):
    """Add two numbers together"""

    total = num1 + num2
    return {"total": total}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
