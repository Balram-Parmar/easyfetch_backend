from fastapi import APIRouter
from app.models import VideoRequest
from app.downloader import run_download

router = APIRouter(
    prefix="/insta",
    tags=["Instagram"]
)

@router.post("/")
async def download_insta_video(request: VideoRequest):
    """
    Downloads a video from Instagram.
    Expects a JSON body: {"url": "..."}
    """
    result = run_download(request.url)
    return result