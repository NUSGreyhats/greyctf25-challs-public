from fastapi import FastAPI

app = FastAPI()


@app.get("/flag")
def read_root():
    return "grey{more_nextjs_server_actions_shenanigans}"
