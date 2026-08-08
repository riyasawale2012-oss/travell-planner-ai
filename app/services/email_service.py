import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.config import settings

class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, html_content: str, text_content: Optional[str] = None) -> bool:
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print(f"[MOCK EMAIL] To: {to_email}, Subject: {subject}")
            return True
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.FROM_EMAIL
            msg["To"] = to_email
            if text_content:
                msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.FROM_EMAIL, to_email, msg.as_string())
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    @staticmethod
    async def send_verification_email(email: str, token: str) -> bool:
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        html = f"""<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; color: white;"><h1>TravelBudget AI</h1><p>Verify your email address</p></div><div style="padding: 30px; background: #f9f9f9;"><p>Hello,</p><p>Thank you for signing up! Please click the button below to verify your email address:</p><div style="text-align: center; margin: 30px 0;"><a href="{verification_url}" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Verify Email</a></div><p>Or copy and paste this link:</p><p style="word-break: break-all; color: #667eea;">{verification_url}</p><p style="color: #666; font-size: 12px;">This link expires in 24 hours.</p></div></body></html>"""
        return await EmailService.send_email(email, "Verify Your Email - TravelBudget AI", html)

    @staticmethod
    async def send_password_reset_email(email: str, token: str) -> bool:
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        html = f"""<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 40px; text-align: center; color: white;"><h1>TravelBudget AI</h1><p>Password Reset Request</p></div><div style="padding: 30px; background: #f9f9f9;"><p>Hello,</p><p>We received a request to reset your password. Click the button below to set a new password:</p><div style="text-align: center; margin: 30px 0;"><a href="{reset_url}" style="background: #f5576c; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a></div><p>If you didn't request this, please ignore this email.</p><p style="color: #666; font-size: 12px;">This link expires in 1 hour.</p></div></body></html>"""
        return await EmailService.send_email(email, "Password Reset - TravelBudget AI", html)
