# 개발 환경 및 테스트 가이드

이 문서는 프로젝트의 가상환경 구성과 노트북 기반 테스트에 대한 일반 지침을 정리한다.

---

## 1. 가상환경 설정

### 1.1 생성 규칙

- 가상환경 이름은 `env-` 접두사를 사용한다 (예: `env-ai`).
- 프로젝트 루트에 생성하며, `.gitignore`에 `env*/` 패턴으로 추적에서 제외한다.
- Python 3.10 이상을 사용한다.

```bash
python3 -m venv env-ai
source env-ai/bin/activate
```

### 1.2 패키지 설치 순서

1. `requirements.txt`의 의존성 설치
2. 프로젝트 패키지를 editable 모드로 설치 (`-e .`)
3. 개발용 도구 설치 (jupyter, ipykernel 등)

```bash
pip install -r requirements.txt
pip install -e .
pip install jupyter ipykernel
```

### 1.3 Jupyter 커널 등록

노트북에서 가상환경을 사용하려면 커널을 등록해야 한다.
`--name`은 가상환경 이름과 동일하게 맞춘다.

```bash
python -m ipykernel install --user --name env-ai --display-name "Python (env-ai)"
```

### 1.4 환경 변수

- `.env.example`에 필요한 환경 변수 템플릿을 유지한다.
- `.env`는 `.gitignore`로 추적에서 제외한다.
- 실제 키 값은 절대 커밋하지 않는다.

```
OPENAI_API_KEY_EUGENE=your_openai_api_key
```

---

## 2. 노트북 테스트

### 2.1 디렉토리 구조

```
notebooks/
├── test_basics.ipynb      # 패키지 기본 함수 동작 확인
├── test_<feature>.ipynb   # 기능별 테스트 노트북
└── experiment_*.ipynb     # 실험/탐색용 노트북
```

### 2.2 노트북 작성 규칙

- **커널**: 반드시 프로젝트 가상환경 커널(`env-ai`)을 선택한다.
- **셀 구성**: 마크다운 셀로 섹션을 나누고, 코드 셀은 하나의 관심사만 다룬다.
- **네이밍**:
  - `test_*.ipynb` — 패키지 함수의 동작 검증 목적
  - `experiment_*.ipynb` — 자유 탐색/프로토타이핑 목적

### 2.3 기본 테스트 노트북 구성 패턴

새 모듈을 추가하면 아래 패턴으로 대응하는 테스트 노트북을 작성한다.

```
1. 패키지/모듈 import 확인
2. 설정값(config) 출력 확인
3. 각 public 함수를 개별 셀에서 호출
4. 정상 응답과 에러 케이스를 각각 확인
```

예시 (test_basics.ipynb):

```python
# Cell 1 — import 확인
import use_ai
print(f"exports: {use_ai.__all__}")

# Cell 2 — config 확인
from use_ai import DEFAULT_MODEL_NAME, AVAILABLE_MODELS
print(f"기본 모델: {DEFAULT_MODEL_NAME}")

# Cell 3 — API 연결 테스트
from use_ai import test_model_connection
result = test_model_connection()
print(result)

# Cell 4 — 프롬프트 호출
from use_ai import prompt_to_model
response = prompt_to_model("테스트 프롬프트", temperature=0.5)
print(response)
```

### 2.4 CLI 실행 (선택)

노트북을 터미널에서 일괄 실행하여 검증할 수도 있다.

```bash
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=60 \
  --ExecutePreprocessor.kernel_name=env-ai \
  notebooks/test_basics.ipynb \
  --output test_basics.ipynb
```

---

## 3. 체크리스트

새 기능을 추가할 때 아래 항목을 확인한다.

- [ ] `requirements.txt`에 신규 의존성 추가
- [ ] `setup.py`의 `install_requires`에도 동일하게 반영
- [ ] 가상환경에 `pip install -r requirements.txt && pip install -e .` 재실행
- [ ] `notebooks/test_<feature>.ipynb` 노트북 작성 및 실행 확인
- [ ] `.env.example`에 신규 환경 변수 템플릿 추가 (필요 시)
