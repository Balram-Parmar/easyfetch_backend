from pydantic import BaseModel

class VideoRequest(BaseModel):
    """
    Defines the expected JSON body for the POST request.
    {"url": "some_video_url"}
    """
    url: str