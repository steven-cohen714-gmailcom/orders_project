from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.endpoints import orders
from backend.database import init_db

# Initialize the database
init_db()

app = FastAPI(
    title="Universal Recycling Purchase Order System",
    description="Purchase Order management system for Universal Recycling"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the orders router
app.include_router(orders.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
