# web_service/web_download.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import yt_dlp, time, os

app = FastAPI()

@app.get("/download")
def download_instagram(url: str = Query(..., description="URL do Instagram")):
    """
    Baixa o vídeo do Instagram (Reel, post, etc) e retorna como arquivo.
    """
    # caminho temporário, único
    tmp_file = f"/tmp/insta_{int(time.time()*1000)}.mp4"
    ydl_opts = {
        "format": "mp4",
        "outtmpl": tmp_file,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        # falha no yt-dlp
        raise HTTPException(status_code=400, detail="❌ Não consegui baixar esse link.")
    # garante que o arquivo foi criado
    if not os.path.exists(tmp_file):
        raise HTTPException(status_code=500, detail="❌ Erro interno ao processar vídeo.")
    # retorna o arquivo para o cliente (download)
    return FileResponse(tmp_file, media_type="video/mp4", filename=os.path.basename(tmp_file))
