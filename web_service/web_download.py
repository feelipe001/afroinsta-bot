# web_service/web_download.py
import os
import time
import yt_dlp
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

app = FastAPI()
DOWNLOAD_TIMER = 5  # segundos de espera

@app.get("/download")
async def download(url: str = Query(..., description="URL completa do Instagram")):
    # opcionalmente, aguardar antes de iniciar
    time.sleep(DOWNLOAD_TIMER)

    # nome único por timestamp
    filename = f"/tmp/insta_{int(time.time()*1000)}.mp4"
    ydl_opts = {
        "format": "mp4",
        "outtmpl": filename,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        # falha no download
        raise HTTPException(status_code=400, detail="Falha ao baixar esse link.")

    # envia o arquivo como resposta
    return FileResponse(filename, media_type="video/mp4", filename="video.mp4")
