from fastapi import FastAPI
from .routes import router
from .models import Base, engine


app = FastAPI()
app.include_router(router)


@app.get("/healthcheck")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    Base.metadata.create_all(engine)


