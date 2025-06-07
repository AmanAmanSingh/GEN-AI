from fastapi import FastAPI



app = FastAPI()


@app.get("/test-server")
def testServer():
    return {status : "success"}