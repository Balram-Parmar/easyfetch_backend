from fastapi import APIRouter
from app.models import VideoRequest
from app.downloader import run_download

router = APIRouter(
    prefix="/yt",  # All routes in this file will start with /yt
    tags=["YouTube"] # Tag for the /docs page
)

@router.post("/")
async def download_yt_video(request: VideoRequest):
    """
    Downloads a video from YouTube.
    Expects a JSON body: {"url": "..."}
    """
    # Call the shared download logic
    result = run_download(request.url)
    return result