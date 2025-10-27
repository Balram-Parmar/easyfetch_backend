import subprocess
import os
from fastapi import HTTPException

# Get the absolute path of the project's root directory
# This file is in /app, so '..' takes us to the root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define paths relative to the project root
VIDEOS_DIR = os.path.join(PROJECT_ROOT, "videos")
YT_DLP_PATH = os.path.join(PROJECT_ROOT, "yt-dlp")
COOKIE_FILE_PATH = os.path.join(PROJECT_ROOT, "cookie.txt") # <-- Path to cookie file

# Ensure the 'videos' directory exists on application startup
os.makedirs(VIDEOS_DIR, exist_ok=True)

def run_download(video_url: str):
    
    """
    Synchronously runs the yt-dlp command to download a video.
    FastAPI will automatically run this sync function in a threadpool
    to avoid blocking the main application.
    """
    
    # Check if the yt-dlp executable exists where we expect it
    if not os.path.isfile(YT_DLP_PATH):
        print(f"Error: yt-dlp executable not found at {YT_DLP_PATH}")
        raise HTTPException(status_code=500, 
                            detail="Server configuration error: yt-dlp executable not found.")

    # Command: ./yt-dlp -4 <url> -P ./videos/
    # -P specifies the output path
    # -4 forces IPv4
    command = [
        YT_DLP_PATH,
        "-4",  # <-- Force IPv4
        video_url,
        "-P",
        VIDEOS_DIR
    ]
    
    # --- New Logic ---
    # Check if the cookie.txt file exists and add it to the command
    if os.path.isfile(COOKIE_FILE_PATH):
        print(f"Using cookie file: {COOKIE_FILE_PATH}")
        command.extend(["--cookies", COOKIE_FILE_PATH])
    else:
        print("cookie.txt not found. Proceeding without cookies.")
    # --- End New Logic ---

    print(f"Executing command: {' '.join(command)}")

    try:
        # Execute the command
        # We set a 10-minute timeout to prevent hangs
        result = subprocess.run(
            command,
            capture_output=True,  # Capture stdout and stderr
            text=True,
            timeout=600,          # 10 minutes
            check=False           # Don't raise an exception on non-zero exit
        )

        if result.returncode == 0:
            # Success!
            print(f"Download successful: {result.stdout}")
            return {"status": "success", "message": "Video download complete.", "log": result.stdout}
        else:
            # Failure
            error_message = f"yt-dlp failed: {result.stderr}"
            print(error_message) # Log to server console
            raise HTTPException(status_code=400, detail=error_message)

    except subprocess.TimeoutExpired:
        print("Error: Download timed out.")
        raise HTTPException(status_code=504, detail="Download timed out after 10 minutes.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")