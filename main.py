from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraping.router import router as scraping_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(scraping_router, prefix="/scraping")

# Configure CORS
origins = [
    "http://localhost:3000",  # Replace with the appropriate origin(s)
    # Add additional origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include your routers and other configurations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

