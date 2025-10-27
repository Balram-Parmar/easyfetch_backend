from fastapi import APIRouter
from app.models import VideoRequest
from app.downloader import run_download

router = APIRouter(
    prefix="/x",
    tags=["X (Twitter)"]
)

@router.post("/")
async def download_x_video(request: VideoRequest):
    """
    Downloads a video from X (Twitter).
    Expects a JSON body: {"url": "..."}
    """
    result = run_download(request.url)
    return result