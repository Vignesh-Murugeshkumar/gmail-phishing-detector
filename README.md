# gmail-phishing-detector
# 🛡️ Phishing Email Scanner using Python

This is a simple Python-based phishing email scanner that connects to your Gmail inbox (and spam folder) using IMAP. It analyzes recent emails to detect potential phishing attempts based on:

 Phishing keywords in the subject
   IP-based URLs in plain text
  Suspicious short links in HTML content

---

 Features

-  Scans both **Inbox** and **Spam**
-  Parses plain text and HTML email content
-  Detects phishing via custom keyword lists and suspicious domains
-  Terminal-based summary output

---

 Requirements

- Python 3.6+
- Gmail IMAP access enabled
- Gmail App Password (not your normal password)

Install dependencies:

```bash
pip install beautifulsoup4
