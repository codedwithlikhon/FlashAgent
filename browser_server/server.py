from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="FlashAgent Browser Server")


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
