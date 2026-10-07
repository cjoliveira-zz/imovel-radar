from fastapi import FastAPI

app = FastAPI(title="ImóvelRadar API", version="0.1.0")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ImóvelRadar API initialized"}
