from fastapi import FastAPI

from src.adapters.inbound.api.item_router import router as item_router


app = FastAPI()
app.include_router(item_router)

@app.get("/health")
def get_health():
    return { "status": "OK" }