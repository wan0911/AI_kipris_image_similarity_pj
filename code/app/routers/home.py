from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import subprocess
from PIL import Image

from fastapi import File, Form, UploadFile
from fastapi.responses import FileResponse

import subprocess
import pickle

# model func
from ..models.simCLR.model import plot_knn_examples, similar_distance
from ..models.ORB_RANSAC import find_matching_features
from ..models.feature_matching.code.main import fm_main


# 절대 경로
BASE_DIR = Path.cwd() / "app"  # app
STATIC_DIR = os.path.join(BASE_DIR, "static/")
IMG_DIR = os.path.join(STATIC_DIR, "img")
INPUT_DIR = os.path.join(IMG_DIR, "input")
OUTPUT_DIR = os.path.join(IMG_DIR, "output")
# model 경로
MODEL_DIR = os.path.join(BASE_DIR, "models/simCLR")
EMBED_DIR = os.path.join(MODEL_DIR, "embeddings.pkl")
print(EMBED_DIR)
FILENAME_DIR = os.path.join(MODEL_DIR, "filenames.pkl")


router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "pages")


@router.get("/home", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse(
        "./home.html", {"request": request, "title": "home"}
    )


@router.post("/upload")
async def img_upload(request: Request, image: UploadFile = File(...)):
    # 이미지 확장자 확인
    img_extension = os.path.splitext(image.filename)[1].lower()
    if img_extension not in [".png", ".jpg", ".jpeg"]:
        return {"error": "Unsupported image format."}

    # 이미지를 img1.png로 저장 (확장자 변경)
    img_filename = "img1.png"
    image_path = os.path.join(INPUT_DIR, img_filename)

    # JPEG 파일을 PNG로 변환하여 저장
    if img_extension == ".jpeg" or img_extension == ".jpg":
        img = Image.open(image.file)
        img.save(image_path, "png")
    else:
        with open(image_path, "wb") as fp:
            fp.write(await image.read())

    print("입력 이미지가 성공적으로 저장되었습니다.")

    # simCLR model 실행
    with open(EMBED_DIR, "rb") as f:
        embeddings_train = pickle.load(f)
    with open(FILENAME_DIR, "rb") as f:
        filenames_train = pickle.load(f)

    model_script_path = str(
        BASE_DIR / "models" / "simCLR" / "model.py"
    )  # model.py 파일의 경로
    process = subprocess.Popen(["python", model_script_path])  # model.py 파일 실행
    process.wait()
    for i in range(1, 6):
        # ORB_RANSAC 실행
        top_matches = find_matching_features(i)
        print(len(top_matches), "갯수 확인")

        if len(top_matches) <= 3:
            fm_main(i)

            print("fm-model이 실행되었습니다.")

    from ..models.simCLR.model import result_data

    # 리다이렉트 수행
    context = {
        "request": request,
        "title": "main",
        "similar_distance": similar_distance,
        "retrieval_data": result_data,
    }

    return templates.TemplateResponse("./main.html", context)


@router.get("/static/images/{file_name}")
def get_image(file_name: str):
    return FileResponse(str(INPUT_DIR / file_name))
