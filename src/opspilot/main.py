from fastapi import FastAPI, HTTPException

from opspilot.api.customers import router as customers_router
from opspilot.api.support_tickets import router as support_tickets_router

app = FastAPI(
    title="OpsPilot API",
    version="0.1.0",
)

app.include_router(customers_router)
app.include_router(support_tickets_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

