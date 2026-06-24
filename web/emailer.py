"""
Sends emails via Gmail SMTP.
Requires env vars: GMAIL_USER, GMAIL_APP_PASSWORD
Get an app password at: myaccount.google.com/apppasswords
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", GMAIL_USER)


def _send(to, subject, body_html):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print(f"[email] No credentials set — skipping: {subject}")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to
        msg.attach(MIMEText(body_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to, msg.as_string())
        return True
    except Exception as e:
        print(f"[email] Failed: {e}")
        return False


def notify_new_subscriber(email, product_name):
    _send(
        NOTIFY_EMAIL,
        f"New price alert signup: {product_name}",
        f"<p><b>{email}</b> signed up for price alerts on <b>{product_name}</b>.</p>"
        f"<p>Total subscribers growing. Keep driving traffic.</p>"
    )


def send_reddit_digest(opportunities):
    if not opportunities:
        return
    rows = ""
    for o in opportunities:
        rows += f"""
        <tr>
          <td style="padding:12px;border-bottom:1px solid #eee;">
            <b><a href="{o['url']}">{o['title']}</a></b><br>
            <span style="color:#888;font-size:13px;">r/{o['subreddit']} · {o['score']} upvotes</span><br><br>
            <b>Suggested reply:</b><br>
            <div style="background:#f5f5f5;padding:10px;border-radius:4px;font-size:13px;">
              {o['suggested_reply']}
            </div>
          </td>
        </tr>"""

    html = f"""
    <h2 style="font-family:sans-serif;">GymPriceWatch — Reddit Opportunities</h2>
    <p style="font-family:sans-serif;color:#555;">
      {len(opportunities)} posts found where you can naturally drop the site.
      Copy-paste the suggested reply, or edit it to sound more like you.
    </p>
    <table style="width:100%;font-family:sans-serif;border-collapse:collapse;">
      {rows}
    </table>
    <p style="font-family:sans-serif;color:#aaa;font-size:12px;">
      GymPriceWatch daily digest
    </p>"""

    _send(NOTIFY_EMAIL, f"Reddit opportunities ({len(opportunities)} found)", html)
