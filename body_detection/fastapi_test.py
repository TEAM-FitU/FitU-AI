from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import io
import base64

app = FastAPI()

# Load YOLO model (사람 탐지 전용)
model = YOLO("yolo12s.pt", task="detect")

def image_to_base64(image_np):
    _, buffer = cv2.imencode('.jpg', image_np)
    return base64.b64encode(buffer).decode('utf-8')

@app.post("/user/profile/image-analysis")
async def analyze_profile_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)
    image_height, image_width = image_np.shape[:2]

    # OpenCV BGR로 변환
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # 추론
    results = model(image_bgr)

    response_data = {
        "person_count": 0,
        "warnings": [],
        "persons": [],
        "annotated_image_base64": None
    }

    for result in results:
        person_boxes = []
        for box in result.boxes:
            if result.names[int(box.cls)] == 'person':
                person_boxes.append(box)

        # 결과 이미지 생성
        annotated = result.plot(boxes=person_boxes)
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        response_data["annotated_image_base64"] = image_to_base64(annotated)

        if person_boxes:
            response_data["person_count"] = len(person_boxes)
            for i, box in enumerate(person_boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_width = x2 - x1
                box_height = y2 - y1
                width_ratio = box_width / image_width
                height_ratio = box_height / image_height

                too_far = width_ratio < 0.5 or height_ratio < 0.5
                if too_far:
                    response_data["warnings"].append(f"Person #{i+1} is too far from the camera.")

                response_data["persons"].append({
                    "id": i + 1,
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                    "too_far": too_far
                })

    return JSONResponse(content=response_data)
