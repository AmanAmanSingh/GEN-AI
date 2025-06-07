from fastapi import FastAPI, Body
from pydantic import BaseModel
import uuid
from .task_queue.connection import queue
from .task_queue.worker import process_query

app = FastAPI()


class chatRequest(BaseModel):
    userId: str | None = None  # for optional
    conversationId: str | None = None
    query: str


@app.get("/test-server")
def testServer():
    return {"status": "success"}


@app.post("/query")
def userQuery(request: chatRequest):

    conversation_id = request.conversationId or str(uuid.uuid4())

    # add queue
    job = queue.enqueue(process_query, request)

    # send user a processing message
    return {
        "status": "processing",
        "message": "Your request is being processed.",
        "job": job.id,
    }
