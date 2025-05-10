
import ttkbootstrap as ttk
import ui.message
from database_logic.auth_db_logic import AuthDBLogic
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv



def foreget_password(parent, window_size, email_var):

    def center_window():
        window.update_idletasks()
        screen_width, screen_height = window_size()
        window_width = window.winfo_width() + 100
        window_height = window.winfo_height()

        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)
        window.geometry(f"+{x_pos}+{y_pos}")


    window = ttk.Toplevel(parent)
    window.title("Return your password")
    window.resizable(False, False)
    center_window()


    label = ttk.Label(window, text='Enter your email address', font="calibri 18 bold", style="info")
    label.pack(pady=20, padx=20)


    entry = ttk.Entry(window, width=50, style="success" ,textvariable=email_var, font="calibri 13 bold")
    entry.pack(padx=20)
    entry.focus_set()

    button = ttk.Button(window, text="Send", cursor="hand2", command=lambda :proccess_sending_password(window, parent ,email_var),
                        style="warning-Outline", padding=10, width=25)
    button.pack(pady=40, padx=20)

    window.bind("<Return>", lambda event: proccess_sending_password(window, parent ,email_var))
    window.grab_set()


def proccess_sending_password(window, parent ,email_var):
    window.destroy()
    email = email_var.get()
    email_var.set("")
    if not email or "@" not in email or "gmail.com" not in email:
        ui.message.MessagePopup(parent, "Error", "Check your inputs", "Please write the right email\nand be carefuly when you write it\nDon not forget @ sign or gmail.com", "danger")
        return

    user = AuthDBLogic().check_email_exists(email)
    if  user is not None:
        send_email(email, user_password=user.password, username=user.username)
        ui.message.MessagePopup(parent, "success", "Check your email inbox", "We sent a message to your email\nit has your password\nDo not worry we here for support you in anytime", "success")
    else:
        ui.message.MessagePopup(parent, "Error", "This email does not exist", "Please check your input\nBecause this email does not exist in the system", 'danger')


def send_email(email, user_password, username):
    load_dotenv()

    sender_email = "mostafabr185@gmail.com"
    receiver_email = email
    password = os.getenv("APP_PASSWORD")  # باسورد التطبيق من جوجل


    # محتوى الرسالة بصيغة HTML
    html_message = f"""
    <html>
    <head>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f9;
          margin: 0;
          padding: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }}
        .email-container {{
          background-color: #ffffff;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
          width: 400px;
          text-align: center;
        }}
        h1 {{
          color: #333333;
        }}
        p {{
          color: #666666;
          font-size: 16px;
        }}
        .password {{
          font-size: 20px;
          color: #e63946;
          font-weight: bold;
          background-color: #f1faee;
          padding: 10px;
          border-radius: 5px;
          display: inline-block;
          margin-top: 20px;
        }}
        .footer {{
          font-size: 12px;
          color: #999999;
          margin-top: 30px;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <h1>Password Reset</h1>
        <p>Dear {username},</p>
        <p>We have received your request to reset your password. Below is your new password:</p>
        <p class="password">{user_password}</p>
        <p>If you did not request this, please ignore this email.</p>
        <div class="footer">
          <p>Thank you for using our service.</p>
        </div>
      </div>
    </body>
    </html>
    """

    # إعدادات الإيميل
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Password"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # أضف المحتوى HTML
    msg.attach(MIMEText(html_message, "html"))


    # إرسال الإيميل
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

