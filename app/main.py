from fastapi import FastAPI
from .routes import router


app = FastAPI()
app.include_router(router)


@app.get("/healthcheck")
def health():
    return {"status": "ok"}



