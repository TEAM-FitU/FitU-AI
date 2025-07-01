# FitU-AI - 의류 스타일링 AI 플랫폼

## 📋 목차
1. [설치 및 설정](#설치-및-설정)
2. [FastAPI 서버 실행 가이드](#fastapi-서버-실행-가이드)
3. [API 엔드포인트 및 요청 예시](#api-엔드포인트-및-요청-예시)
4. [모델 다운로드](#모델-다운로드)

## 🚀 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
최상위 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here

# FASHN API 키
FASHN_API_KEY=your_fashn_api_key_here

# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# AWS 설정 (S3 사용 시)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=ap-northeast-2
```

## 🖥️ FastAPI 서버 실행 가이드

### 1. 사람 탐지
```bash
# body_detection 디렉토리로 이동
cd body_detection

# 서버 실행 (포트 8000)
uvicorn fastapi_test:app --reload --host 0.0.0.0 --port 8000
```

**접속 URL**: http://localhost:8000/docs

### 2. 코디 추천 & 가상 피팅
```bash
# GPT 디렉토리로 이동
cd GPT

# 서버 실행 (포트 8001)
uvicorn aws_api:app --reload --host 0.0.0.0 --port 8001
```

**접속 URL**: http://localhost:8001/docs

### 3. 의류 이미지 분석
```bash
# 데이터셋/옷 종류 분류/test 디렉토리로 이동
cd "데이터셋/옷 종류 분류/test"

# 서버 실행 (포트 8002)
uvicorn fastapi:app --reload --host 0.0.0.0 --port 8002
```

**접속 URL**: http://localhost:8002/docs

## 📡 API 엔드포인트 및 요청 예시

### 1. 사람 탐지 API (`body_detection/fastapi_test.py`)

#### 엔드포인트: `POST /user/profile/image-analysis`

**기능**: 프로필 이미지에서 사람을 탐지하고 적절성 검증

**요청 예시**:
```json
{
  "s3_url": "https://example-bucket.s3.amazonaws.com/profile-image.jpg"
}
```

**응답 예시**:
```json
{
  "warnings": [
    "인물이 너무 멀리 있습니다. 가까이 와주세요."
  ]
}
```

**가능한 경고 메시지**:
- `"사람이 탐지되지 않았습니다."` - 사람이 이미지에 없음
- `"한 명만 나와야 합니다. 현재 인원: 2"` - 여러 명이 감지됨
- `"인물이 너무 멀리 있습니다. 가까이 와주세요."` - 인물이 너무 작게 촬영됨

---

### 2. 코디 추천 & 가상 피팅 API (`GPT/aws_api.py`)

#### 엔드포인트: `POST /vision/recommendation`

**기능**: 상황과 날씨에 맞는 의류 조합 추천

**요청 예시**:
```json
{
  "user_id": "user123",
  "situation": "여행",
  "targetTime": "2025년 06월 25일",
  "targetPlace": "제주도",
  "highTemperature": 25,
  "lowTemperature": 18,
  "rainPercent": 0,
  "status": "맑음",
  "showClosetOnly": true
}
```

**응답 예시**:
```json
{
  "header": {
    "resultCode": "00",
    "resultMsg": "SUCCESS"
  },
  "body": {
    "summary": "2025년 06월 25일에 제주도에서 여행을 위한 스타일링",
    "weather": "맑음, 21°C, 강수확률: 0%",
    "result": [
      {
        "combination": "상의: 티셔츠, 하의: 청바지",
        "selected": "001 (TSHIRT) + 002 (JEANS)",
        "reason": "제주도 여행에 적합한 캐주얼한 조합입니다. 21°C의 맑은 날씨에 편안하면서도 스타일리시한 룩을 연출할 수 있습니다.",
        "virtualTryonImage": "https://example.com/virtual-tryon-result-1.jpg",
        "virtualTryonError": null,
        "clothing_links": [
          {
            "id": "001",
            "category": "TSHIRT",
            "image_url": "https://example.com/tshirt.jpg"
          },
          {
            "id": "002",
            "category": "JEANS",
            "image_url": "https://example.com/jeans.jpg"
          }
        ]
      },
      {
        "combination": "상의: 셔츠, 하의: 바지",
        "selected": "003 (SHIRT) + 004 (PANTS)",
        "reason": "여행 중에도 깔끔한 이미지를 유지할 수 있는 조합입니다. 통기성이 좋은 소재로 편안함을 제공합니다.",
        "virtualTryonImage": "https://example.com/virtual-tryon-result-2.jpg",
        "virtualTryonError": null,
        "clothing_links": [
          {
            "id": "003",
            "category": "SHIRT",
            "image_url": "https://example.com/shirt.jpg"
          },
          {
            "id": "004",
            "category": "PANTS",
            "image_url": "https://example.com/pants.jpg"
          }
        ]
      }
    ]
  }
}
```

**요청 파라미터 설명**:
- `user_id`: 사용자 고유 ID
- `situation`: 상황 (회사 출근, 데이트, 운동 등)
- `targetTime`: 목표 시간
- `targetPlace`: 목표 장소
- `highTemperature`: 최고 기온
- `lowTemperature`: 최저 기온
- `rainPercent`: 강수 확률 (0-100)
- `status`: 날씨 상태 (맑음, 흐림, 비, 눈, 안개, 일반 등)
- `showClosetOnly`: 옷장에 있는 옷만 사용할지 여부

**응답 필드 설명**:
- `header`: API 응답 상태 정보
  - `resultCode`: "00" (성공), "01" (실패)
  - `resultMsg`: 응답 메시지
- `body`: 실제 추천 결과
  - `summary`: 전체 추천 요약
  - `weather`: 날씨 정보 (상태, 평균기온, 강수확률)
  - `result`: 추천 조합 목록
    - `combination`: 조합 설명 (한국어)
    - `selected`: 선택된 옷 ID 및 종류
    - `reason`: 추천 이유
    - `virtualTryonImage`: 가상 피팅 결과 이미지 URL
    - `virtualTryonError`: 가상 피팅 오류 메시지 (성공 시 null)
    - `clothing_links`: 옷 정보 링크
      - `id`: 옷 ID (가상 옷인 경우 null)
      - `category`: 옷 종류
      - `image_url`: 옷 이미지 URL

---

### 3. 의류 이미지 분석 API (`데이터셋/옷 종류 분류/test/fastapi.py`)

#### 엔드포인트: `POST /clothes/image-analysis`

**기능**: 의류 이미지 분석 (종류, 패턴, 톤 분류)

**요청 예시**:
```json
{
  "s3_url": "https://example-bucket.s3.amazonaws.com/clothing-image.jpg"
}
```

**응답 예시**:
```json
{
  "status": "single_cloth",
  "analyses": [
    {
      "category": "top",
      "subcategory": "티셔츠",
      "pattern": "플레인",
      "tone": "밝은 톤",
      "segmented_image_path": "https://example.com/segmented-image.jpg"
    }
  ]
}
```

**응답 상태값**:
- `"no_clothes"`: 옷이 탐지되지 않음
- `"single_cloth"`: 1개의 옷이 탐지됨
- `"multiple_clothes"`: 2개 이상의 옷이 탐지됨

**분류 가능한 카테고리**:
- **상의 (top)**: 티셔츠, 셔츠, 블라우스, 가디건, 코트, 자켓, 점퍼, 스웨터, 베스트
- **하의 (bottom)**: 청바지, 바지, 반바지, 치마, 슬랙스, 활동복
- **원피스 (onepiece)**: 드레스, 점프수트

**패턴 분류**:
- 플레인, 체크, 스트라이프, 도트, 플로럴, 기하학, 동물, 심볼, 기타

**톤 분류**:
- 밝은 톤, 어두운 톤

## 📥 모델 다운로드

다운받은 모델은 `데이터셋/옷 종류 분류/model` 디렉토리에 저장하세요.

### 필수 모델 파일들:

1. **[사람 탐지 모델 (YOLO)](https://drive.google.com/file/d/1kX1hK0drSZJ3S-beBcVVin6HHN2rN04o/view?usp=sharing)**
   - 파일명: `yolo12s.pt`
   - 위치: `body_detection/obstacle_detect_yolo12s.onnx`

2. **[상의/하의/원피스 분류 모델](https://drive.google.com/file/d/1NMrXK98VV1opBPCO6e3tT5QGB_bHg0Mb/view?usp=sharing)**
   - 파일명: `classification_efficientnetv2_s.pt`

3. **[패턴 분류 모델](https://drive.google.com/file/d/1a9mXbCGYCf8TrJOoWjsyWiZznisjQJgt/view?usp=sharing)**
   - 파일명: `clothes_pattern.pt`

4. **[세그멘테이션 모델](https://drive.google.com/file/d/104BQohKt7zcYzibFhOveO9eDDb3I0kHu/view?usp=sharing)**
   - 파일명: `segmentation_model.pt`

## 🔧 문제 해결

### 포트 충돌 시
다른 포트를 사용하여 서버를 실행하세요:
```bash
uvicorn filename:app --reload --host 0.0.0.0 --port 8003
```

### 모델 파일 경로 오류 시
각 서버의 모델 파일 경로를 확인하고 필요시 수정하세요.

### API 키 오류 시
`.env` 파일의 API 키가 올바르게 설정되었는지 확인하세요.

## 📞 지원

문제가 발생하거나 추가 도움이 필요하시면 개발팀에 문의하세요.
