# PhysiqAI Backend

> **상태: 개발 중단 (실험 기록용 공개)**
> 논문 근거 기반 규칙 시스템으로 운동·식단·생활 습관을 추천하고, 데이터가 쌓이면 개인 맞춤으로 확장하려던 프로젝트입니다. 데이터 확보와 근거 검증의 한계로 중단했고, 그 과정과 배운 점을 아래에 정리했습니다.

## 프로젝트 목표
1. **1단계: 규칙 기반 추천** — 논문에서 정리한 규칙을 전문가 시스템(Expert System)으로 구현해 헬스 운동, 식단, 생활 로그를 추천
2. **2단계: 개인 맞춤화** — 사용자의 기록 데이터가 쌓이면 그 데이터로 추천을 개인에 맞게 조정

## 기술 스택
- Python, FastAPI
- PostgreSQL 16 (Docker), SQLAlchemy 2.0 (async, asyncpg), Alembic (마이그레이션)
- Supabase
- experta (규칙 기반 전문가 시스템)
- Anthropic Claude API
- JWT 인증 (python-jose, passlib)
- pytest

## 구조
```
app/
├─ core/           설정, DB·Supabase 연결, 인증·보안, 의존성
├─ expert_system/  규칙 기반 추천 엔진 (engine, facts)
├─ models/         DB 모델 (사용자, 운동, 식단, 수면, 인바디, 주간 리포트)
├─ routers/        API 엔드포인트
├─ schemas/        요청·응답 스키마
├─ services/       Claude 연동 서비스
└─ main.py
alembic/           DB 마이그레이션
tests/             테스트
docker-compose.yml 로컬 개발용 PostgreSQL
```

## 구현한 것
**API 라우터**
- 사용자 (`users`), 인증 (JWT)
- 운동 기록 (`workouts`)
- 식단 기록 (`diet_logs`)
- 수면 기록 (`sleep_logs`)
- 체성분(인바디) 기록 (`inbody`)
- 주간 리포트 (`weekly_reports`)
- AI 코치 (`ai_coach`, Claude 연동)
- 헬스 체크 (`health`) 및 테스트

**규칙 기반 추천 엔진**
- experta 기반 추천 엔진 (`engine`, `facts`)

**기반 구조**
- SQLAlchemy 모델과 Alembic 마이그레이션
- Docker 기반 로컬 PostgreSQL 환경
- 환경 변수 기반 설정 (키는 `.env`로 분리, `.env.example` 제공)

## 중단한 이유
1. **데이터 축적에 시간이 너무 오래 걸림**: 개인 맞춤화는 사용자 기록 데이터가 쌓여야 가능한데, 의미 있는 양이 모이기까지의 시간이 현실적이지 않았다.
2. **규칙의 근거가 되는 논문 확보의 한계**: 논문 약 80~90편을 수집했지만 규칙 체계를 만들기에는 양이 부족했다.
3. **근거 검증의 어려움**: 논문 하나하나의 신뢰도와 연구 설계를 검증하기 어려웠고, 신뢰도가 높은 논문일수록 접근이 어려운 경우가 많았다.

## 배운 점
- 개인 맞춤 AI는 모델보다 **데이터를 어떻게 확보할지**를 먼저 설계해야 한다.
- 건강·운동 같은 분야의 규칙은 **근거의 질**이 핵심이라, 수집량보다 검증 가능한 소수의 근거에서 시작하는 편이 현실적이다.
- 시작 전에 **데이터 확보 계획과 검증 기준**을 정해 두면 같은 시행착오를 줄일 수 있다.

## 만약 다시 한다면
- 공신력 있는 기관의 운동·영양 권고처럼 접근 가능하고 검증된 자료에서 규칙을 시작한다.
- 사용자 데이터 없이도 검증할 수 있는 작은 범위로 먼저 만들고 평가 기준을 정한다.

## 실행 (로컬)
```bash
docker compose up -d          # PostgreSQL 실행 (로컬 개발용 설정)
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
# .env.example을 복사해 .env를 만들고 값을 채운다
alembic upgrade head
uvicorn app.main:app --reload
pytest
```
