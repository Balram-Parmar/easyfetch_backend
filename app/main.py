from fastapi import FastAPI
from app.routers import yt, insta, x

app = FastAPI(
    title="Video Downloader API",
    description="An API to download videos from various platforms using yt-dlp.",
    version="1.0.0"
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