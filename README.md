# FitU-AI

1. requirements.txt 설치

2. 최상위 디렉토리에 .env 파일을 만들고 아래 입력

```
OPENAI_API_KEY= YOUR_API_KEY
FASHN_API_KEY= YOUR_API_KEY
```

키는 제작자에게 요청 혹은 직접 사용

## 모델 다운로드
다운받은 모델은 '데이터셋/옷 종류 분류/model' 에 넣으면 됩니다.

[사람 탐지 (기본 모델)](https://drive.google.com/file/d/1kX1hK0drSZJ3S-beBcVVin6HHN2rN04o/view?usp=sharing)

[상의, 하의, 원피스 분류 모델](https://drive.google.com/file/d/1NMrXK98VV1opBPCO6e3tT5QGB_bHg0Mb/view?usp=sharing)

[상의 종류 분류 모델](https://drive.google.com/file/d/104BQohKt7zcYzibFhOveO9eDDb3I0kHu/view?usp=sharing)

[하의 종류 분류 모델](https://drive.google.com/file/d/1MB2q8uDRkU3TorO6MjQggqOdlEir11lw/view?usp=sharing)

[원피스 종류 분류 모델](https://drive.google.com/file/d/13KApx6cHOwbyPx5JLTLWVwn2g5DQWXUy/view?usp=sharing)

[패턴 분류 모델](https://drive.google.com/file/d/1a9mXbCGYCf8TrJOoWjsyWiZznisjQJgt/view?usp=sharing)

## 실행법 (streamlit)
### GPT

콘솔창에 `streamlit run 'GPT/streamlit_test.py'`

### 옷 자동 분류 & Try_on

콘솔창에 `streamlit run '데이터셋/옷 종류 분류/test/app.py'`

### 사람 탐지

콘솔창에 `streamlit run 'body_detection/body_detection_test.py'`

