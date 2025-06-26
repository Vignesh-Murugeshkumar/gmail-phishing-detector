import imaplib
import re
import email
from bs4 import BeautifulSoup

# ==== CONFIGURATION ====
emailAccount = "your-email@gmail.com"
appPassword = "your-16-digit-app-password"
imapServer = "imap.gmail.com"
imapPort = 993

phishingKeywords = [
    "verify", "update", "suspend", "urgent", "immediate", "password",
    "login", "expire", "reset", "accept money", "send money"
]
suspiciousLinks = ["bit.ly", "tinyurl", "ow.ly"]

# ==== FUNCTIONS ====

def connectToGmail():
    mail = imaplib.IMAP4_SSL(imapServer, imapPort)
    mail.login(emailAccount, appPassword)
    return mail

def fetchData(mail, emailLimit=5):
    result, data = mail.search(None, "ALL")
    emailIds = data[0].split()[-emailLimit:]
    return emailIds

def checkSubject(subject):
    return any(word in subject.lower() for word in phishingKeywords)

def checkIPLinks(text):
    return bool(re.findall(r'https?://\d{1,3}(?:\.\d{1,3}){3}', text))

def checkSuspiciousLinks(html):
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a', href=True):
        if any(domain in link['href'] for domain in suspiciousLinks):
            return True
    return False

def checkEmail(rawEmail):
    msg = email.message_from_bytes(rawEmail)
    subject = msg.get('subject', '(No Subject)')
    fromEmail = msg.get('from', '(Unknown Sender)')
    plainText = ""
    htmlcontent = ""

    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == "text/plain":
            try:
                plainText += part.get_payload(decode=True).decode(errors='ignore')
            except:
                continue
        elif content_type == "text/html":
            try:
                htmlcontent += part.get_payload(decode=True).decode(errors='ignore')
            except:
                continue

    # Check for phishing indicators
    flags = []
    if checkSubject(subject):
        flags.append(" Phishing keyword in subject")
    if checkIPLinks(plainText):
        flags.append(" IP-based URL in plain text")
    if checkSuspiciousLinks(htmlcontent):
        flags.append("Suspicious short link in HTML")

    # Output Results
    print("=" * 50)
    print(f"From: {fromEmail}")
    print(f"Subject: {subject}")
    if flags:
        print("PHISHING DETECTED:")
        for f in flags:
            print(f" - {f}")
    else:
        print(" Email appears safe")
    print("=" * 50)

# ==== MAIN FUNCTION ====

if __name__ == "__main__":
    mail = connectToGmail()

    # Loop through Inbox and Spam
    for folder in ["INBOX", "[Gmail]/Spam"]:
        print(f"\nScanning folder: {folder}")
        try:
            mail.select(folder)
            emailIds = fetchData(mail)
            for emailId in emailIds:
                res, data = mail.fetch(emailId, "(RFC822)")
                rawEmail = data[0][1]
                checkEmail(rawEmail)
        except Exception as e:
            print(f" Error accessing {folder}: {e}")

    try:
        mail.close()
    except:
        pass
    mail.logout()
