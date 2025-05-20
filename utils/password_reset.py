
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import ttkbootstrap as ttk
from display_messages.message_popup import MessagePopup
from db.db_auth.auth_db import AuthDB
import socket

def forget_password(parent, window_size, email_var):
    def center_window():
        window.update_idletasks()
        screen_width, screen_height = window_size()

        window_width = window.winfo_width()
        window_height = window.winfo_height()

        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)
        window.geometry(f"+{x_pos}+{y_pos}")

    window = ttk.Toplevel(parent)
    window.title("Reset Your Password")
    window.resizable(False, False)
    window.iconbitmap(False,  os.path.join("assets", "logo.ico"))



    ttk.Label(window, text='Enter your email address', font="calibri 18 bold", style="info").pack(pady=20, padx=20)

    entry = ttk.Entry(
        window, width=50, style="success",
        textvariable=email_var, font="calibri 13 bold"
    )
    entry.pack(padx=30)
    entry.focus_set()

    ttk.Button(
        window, text="Send", cursor="hand2",
        command=lambda: handle_password_request(window, parent, email_var),
        style="warning-Outline", padding=10, width=25
    ).pack(pady=40, padx=20)

    window.bind("<Return>", lambda event: handle_password_request(window, parent, email_var))
    window.grab_set()
    center_window()



def handle_password_request(window, parent, email_var):
    window.destroy()
    email = email_var.get().strip()
    email_var.set("")

    if not email or "@" not in email or not email.endswith("@gmail.com"):
        MessagePopup(
            parent, "Invalid Email", "Email Format Error",
            "Please enter a valid Gmail address.\nExample: example@gmail.com",
            "danger"
        )
        return

    user = AuthDB().is_email_taken(email)
    if user:
        send_password_email(parent, email, user.username, user.password)
        MessagePopup(
            parent, "Success", "Email Sent",
            "A message with your password has been sent to your inbox.",
            "success"
        )
    else:
        MessagePopup(
            parent, "Email Not Found", "User Not Registered",
            "No account is associated with this email address.",
            "danger"
        )

def send_password_email(root, to_email, username, password):
    load_dotenv()

    from_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔐 Your Password Recovery"
    msg["From"] = from_email
    msg["To"] = to_email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px;">
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
          <h2 style="color: #333;">Hello {username},</h2>
          <p>You requested a password reset. Here is your password:</p>
          <p style="font-size: 18px; color: #d62828; font-weight: bold; background-color: #f1f1f1; padding: 10px; border-radius: 5px;">{password}</p>
          <p>If you didn’t make this request, please ignore this email or contact support.</p>
          <hr style="margin-top: 30px;">
          <p style="font-size: 12px; color: #777;">This email was sent automatically. Please do not reply.</p>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, app_password)
            server.send_message(msg)
            server.quit()

    except socket.gaierror:
        MessagePopup(
            root,
            "Error",
            "Internet Connection Error",
            "There is no connection to the internet.\nPlease check your connection and try again.",
            "danger"
        )

    except smtplib.SMTPException:
        MessagePopup(
            root,
            "Error",
            "Email Sending Error",
            f"An error occurred while sending the email\nTry again later",
            "danger"
        )
