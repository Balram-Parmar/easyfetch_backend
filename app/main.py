from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import yt, insta, x

app = FastAPI(
    title="Video Downloader API",
    description="An API to download videos from various platforms using yt-dlp.",
    version="1.0.0"
)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the routers from the separate files
app.include_router(yt.router)
app.include_router(insta.router)
app.include_router(x.router)

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for health check.
    """
    return {"message": "Welcome to the Video Downloader API. Visit /docs for API documentation."}