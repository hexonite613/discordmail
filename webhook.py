import imaplib
import email
from email.header import decode_header
import requests
import time
import os
import re
from dotenv import load_dotenv

load_dotenv()

# 네이버 메일 계정 정보
EMAIL_ACCOUNT = os.getenv("Email_ID")
EMAIL_PASSWORD = os.getenv("PW")
IMAP_SERVER = "imap.naver.com"

# 디스코드 웹훅 URL
DISCORD_WEBHOOK_URL = os.getenv("discord_webhook")

# 알림을 보낼 이메일 도메인 목록
ALLOWED_DOMAINS = ["@gmail.com", "@naver.com", "@hanyang.ac.kr"]

# 메일 확인 함수
def check_mail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")  # 받은메일함

    # 'UNSEEN' == 읽지 않은 메일 확인
    result, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()

    new_mails = []
    for num in mail_ids:
        # UID 가져오기
        result, uid_data = mail.fetch(num, "(UID)")
        uid_match = re.search(r"UID (\d+)", str(uid_data))
        mail_uid = uid_match.group(1) if uid_match else None

        # 메일 본문 가져오기
        result, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # 제목 디코딩
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes) and encoding:
                    subject = subject.decode(encoding)

                # 보낸사람 확인
                from_email = msg.get("From")

                # 이메일 주소만 추출 (정규표현식)
                match = re.search(r"<(.+?)>", from_email)
                email_address = match.group(1) if match else from_email

                # 보낸 사람이 허용된 도메인이 아니면 스킵
                if not any(email_address.endswith(domain) for domain in ALLOWED_DOMAINS):
                    continue

                # 네이버 메일 웹 URL 생성 (UID 사용)
                if mail_uid:
                    mail_url = f"https://mail.naver.com/v2/read/-1/{mail_uid}"
                else:
                    mail_url = "https://mail.naver.com"  # 기본 링크

                new_mails.append((subject, email_address, mail_url))

                # 메일 읽음 상태로 변경 (중복 알림 방지)
                mail.store(num, "+FLAGS", "\\Seen")

    mail.logout()
    return new_mails

# 디스코드로 알림 보내기
def send_to_discord(subject, from_email, mail_url):
    data = {
        "content": f"📧 **새 이메일 도착!**\n**제목:** {subject}\n**보낸사람:** {from_email}\n🔗 [메일 확인하기]({mail_url})"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# 주기적으로 메일 확인
while True:
    mails = check_mail()
    for subject, from_email, mail_url in mails:
        send_to_discord(subject, from_email, mail_url)
    time.sleep(10)  # 1분마다 확인