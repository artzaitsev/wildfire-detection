from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
app = FastAPI()

# Подключаем React-статические файлы
app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="web/dist/static"), name="static")

@app.get("/api/v1/predict")
async def api_root():
    return {"message": "API работает"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse("web/dist/index.html")