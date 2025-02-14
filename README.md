# 📧 Naver Mail to Discord Webhook

네이버 메일에서 특정 발신자로 온 새 이메일을 감지하고 디스코드 웹훅으로 전송하는 Python 스크립트

---

## 🚀 기능

✅ 네이버 메일의 읽지 않은 메일 확인\
✅ 특정 도메인(@gmail.com, @naver.com, @hanyang.ac.kr)에서 온 메일만 알림(코드 수정시 다른 도메인 가능)\
✅ 디스코드 웹훅으로 알림 전송\
✅ 실제 네이버 메일 읽기 링크 포함

---

## 📌 설치 방법

### 1️⃣ Python & 필수 패키지 설치

```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install requests
```

### 3️⃣ 환경 설정 (메일 계정 및 웹훅 수정)

`your_script.py` 파일을 열고, 다음 값을 수정하세요:

```python
EMAIL_ACCOUNT = "your_id"
(네이버 ID)
EMAIL_PASSWORD = "your_app_password"
(네이버 비번)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_id"
(디스코드 웹훅 발급받은 URL)
```

📌 **네이버 비밀번호를 사용해야 합니다!**

---

## ▶ 실행 방법

### 1️⃣ 일반 실행

```bash
python3 your_script.py
```

### 2️⃣ 백그라운드 실행 (`nohup`)

```bash
nohup python3 webhook.py > output.log 2>&1 &
```

📌 실행 후 `output.log`에서 로그를 확인할 수 있습니다.

---

## ⏹ 종료 방법

```bash
pkill -f your_script.py
```

또는

```bash
kill $(pgrep -f webhook.py)
```

---


## 🔧 디스코드 웹훅 설정 방법

1. 디스코드 서버에서 `설정 > 통합`으로 이동
2. "웹훅 만들기" 클릭 후 URL 복사
3. `your_script.py`의 `DISCORD_WEBHOOK_URL`에 붙여넣기

---

이제 네이버 메일 알림을 디스코드에서 받아보세요! 🚀

