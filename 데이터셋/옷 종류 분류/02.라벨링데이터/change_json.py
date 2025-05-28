import os
import json
from glob import glob

# 입력 폴더와 출력 파일 경로를 지정하세요
INPUT_DIR = '데이터셋/옷 종류 분류/02.라벨링데이터/TL_상품_하의_onepiece(jumpsuite)'
OUTPUT_FILE = '데이터셋/옷 종류 분류/02.라벨링데이터/TL_상품_하의_onepiece(jumpsuite)/total_coco.json'
CATEGORY_NAME = 'onepiece(jumpsuite)'

# COCO 포맷 기본 구조
coco = {
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 1, "name": CATEGORY_NAME}
    ]
}

image_id = 1
annotation_id = 1

json_files = glob(os.path.join(INPUT_DIR, '*.json'))

for json_path in json_files:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이미지 정보
    file_name = os.path.basename(data['dataset']['dataset.image_path'])
    width = int(data['dataset']['dataset.width'])
    height = int(data['dataset']['dataset.height'])

    coco['images'].append({
        "id": image_id,
        "file_name": file_name,
        "width": width,
        "height": height
    })

    # annotation(폴리곤) 정보
    for ann in data['annotation']:
        if ann.get('annotation_type') != 'Polygon':
            continue
        points = ann['annotation_point']
        # COCO는 [ [x1, y1, x2, y2, ...] ] 형태로 segmentation 저장
        segmentation = [points]
        # bbox 계산 (xmin, ymin, w, h)
        xs = points[0::2]
        ys = points[1::2]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        bbox = [xmin, ymin, xmax - xmin, ymax - ymin]
        area = (xmax - xmin) * (ymax - ymin)
        coco['annotations'].append({
            "id": annotation_id,
            "image_id": image_id,
            "category_id": 1,
            "segmentation": segmentation,
            "bbox": bbox,
            "area": area,
            "iscrowd": 0
        })
        annotation_id += 1
    image_id += 1

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(coco, f, ensure_ascii=False, indent=2)

print(f"변환 완료! {OUTPUT_FILE} 파일이 생성되었습니다.") 