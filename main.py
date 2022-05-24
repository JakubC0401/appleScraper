from fastapi import FastAPI

app = FastAPI()

@app.get("/euro")
async def ShowEuroData():
    return "hello"

@app.get("/")
async def ShowEuroData():
    return "Main"

