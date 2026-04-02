import smtplib
from email.message import EmailMessage

def draft_negotiation_email(item_title, shortfall, revenue_at_risk, current_price):
    """Drafts the email body based on inventory risk metrics."""
    discount_ask = "15%" if revenue_at_risk > 500 else "5%"
    return f"""Subject: Urgent Restock Request: {item_title}

Dear Vendor Team,

Our system identifies a critical stockout risk for "{item_title}".
- Predicted Shortfall: {shortfall} units
- Revenue at Risk: ${revenue_at_risk}

We need to order {shortfall} units immediately. Given the urgency and volume, can you offer a {discount_ask} discount or expedited shipping?

Best,
Warehouse AI Agent"""

def send_negotiation_email(recipient_email, body):
    """Sends the email using the App Password."""
    sender_email = "bharatpchandran@gmail.com"  # Your Gmail address
    app_password = "kfat ktit pjkg zopn"   # Paste your 16-character code here

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Urgent Restock Request & Quote Inquiry"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Port 465 is for SMTP over SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Dispatch failed: {str(e)}"