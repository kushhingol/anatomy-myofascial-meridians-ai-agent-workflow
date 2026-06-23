import os
import json
import argparse
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from google import genai
from google.genai import types
from email.message import EmailMessage

# Automatically load environment settings from a local .env file if it exists
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini Client
client = genai.Client()

def calculate_adaptive_time(completed_count):
    weeks = completed_count // 7
    if weeks <= 1: return 15
    elif weeks <= 3: return 20
    elif weeks <= 5: return 25
    elif weeks <= 7: return 30
    elif weeks <= 9: return 40
    elif weeks <= 11: return 50
    else: return 60

def convert_md_to_styled_html(md_content, topic_name, completed_lessons):
    """Converts raw markdown into an elegant, email-client-friendly HTML layout with a history log."""
    # Using 'tables' only, standard lists are supported natively by core markdown
    raw_html = markdown.markdown(md_content, extensions=['tables'])
    
    if completed_lessons:
        history_items = "".join([f"<li>{lesson}</li>" for lesson in completed_lessons])
    else:
        history_items = "<li>Starting journey today!</li>"

    email_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic_name}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f4f6f8;
                color: #333333;
                margin: 0;
                padding: 0;
            }}
            .wrapper {{
                width: 100%;
                background-color: #f4f6f8;
                padding: 20px 0;
            }}
            .container {{
                max-width: 650px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                overflow: hidden;
                border: 1px solid #e1e4e8;
            }}
            .header {{
                background: linear-gradient(135deg, #1e3a8a, #3b82f6);
                color: #ffffff;
                padding: 30px 25px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 700;
            }}
            .header p {{
                margin: 5px 0 0 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px 25px;
                line-height: 1.6;
                font-size: 16px;
            }}
            h2 {{
                color: #1e3a8a;
                font-size: 20px;
                border-bottom: 2px solid #eff6ff;
                padding-bottom: 8px;
                margin-top: 30px;
            }}
            h3 {{
                color: #2563eb;
                font-size: 18px;
                margin-top: 20px;
            }}
            p {{
                margin: 0 0 15px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #e2e8f0;
                padding: 10px 12px;
                text-align: left;
                font-size: 14px;
            }}
            th {{
                background-color: #f1f5f9;
                color: #1e3a8a;
            }}
            .dashboard-box {{
                margin-top: 40px;
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 20px;
            }}
            .dashboard-box h4 {{
                margin: 0 0 10px 0;
                color: #1e3a8a;
                font-size: 15px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 5px;
            }}
            .dashboard-box ul {{
                margin: 0;
                padding-left: 20px;
                font-size: 13px;
                color: #475569;
            }}
            .dashboard-box li {{
                margin-bottom: 4px;
            }}
            .footer {{
                background-color: #f8fafc;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                <div class="header">
                    <p>MPT POSTGRADUATER PHYSIOTHERAPY EDUCATION CURRICULUM</p>
                    <h1>{topic_name}</h1>
                </div>
                <div class="content">
                    {raw_html}
                    
                    <div class="dashboard-box">
                        <h4>Completed Modules Summary ({len(completed_lessons)} Completed)</h4>
                        <ul>
                            {history_items}
                        </ul>
                    </div>
                </div>
                <div class="footer">
                    <p>Automated Structural Integration Learning Stack • Anatomy Trains Journey</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return email_template

def send_email(subject: str, html_body: str) -> bool:
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "MAIL_FROM", "MAIL_TO"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        print(f"Email not sent. Missing environment variables: {', '.join(missing)}")
        return False
    
    # 1. Parse and sanitize the comma-separated string into a clean list of strings
    raw_mail_to = os.environ["MAIL_TO"]
    to_addresses = [email.strip() for email in raw_mail_to.split(",") if email.strip()]
    
    if not to_addresses:
        print("Email not sent. MAIL_TO does not contain any valid email addresses.")
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ["MAIL_FROM"]
    # 2. Join them back with a comma for a clean header display in the email client
    msg["To"] = ", ".join(to_addresses)
    msg.add_alternative(html_body, subtype="html")

    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        smtp.send_message(msg)
    print(f"Email sent to {', '.join(to_addresses)}")
    return True




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args()

    with open("progress.json", "r") as f:
        progress = json.load(f)
        
    completed_lessons = progress.get("completedLessons", [])
    weak_topics = progress.get("weakTopics", [])
    target_minutes = calculate_adaptive_time(len(completed_lessons))
    
    # Initialize startDate if not present
    if "startDate" not in progress:
        progress["startDate"] = datetime.now().strftime("%Y-%m-%d")
    
    # Calculate daysElapsed from start date
    start_date = datetime.strptime(progress["startDate"], "%Y-%m-%d").date()
    today = datetime.now().date()
    days_elapsed = (today - start_date).days
    
    # Calculate currentPhase based on daysElapsed (Phase 1: days 0-6, Phase 2: days 7-13, etc.)
    current_phase = (days_elapsed // 7) + 1
    
    pdf_path = "Anatomy_Trains_Myofascial_Meridians_for_Manual_&_Movement_Therapists.pdf"
    book_file = client.files.upload(file=pdf_path)

    system_instruction = f"""
    You are an expert Physiotherapy Education AI specializing in Anatomy Trains, Myofascial Meridians, and Structural Integration.
    Generate a daily lesson matching a {target_minutes}-minute masterclass lecture standard based strictly on the provided file.
    Use advanced clinical terminology suitable for an MPT postgraduate student.
    Ensure sections are structured visually using descriptive headers, bold callouts, markdown lists, and data comparison tables.
    """

    # Updated prompt layout structure to explicitly pull answers out of the quiz and place them at the end
    user_prompt = """
    Generate today's daily lesson based on the student's current learning history. Include all core components exactly in this sequential order:
    ### Today's Topic
    ### Brief Summary
    ### Core Learning Content
    ### Key Concepts
    ### Clinical Relevance
    ### Case Example
    ### Movement Assessment Insight
    ### Key Takeaways
    
    ### Quiz
    (Generate 5 comprehensive, highly analytical clinical multiple-choice questions here with options A, B, C, D. Do NOT reveal the correct answers or explanations inside this section so the student can test themselves fairly).
    
    ### Reflection Question
    
    ### Tomorrow's Preview
    
    ### Quiz Answers & Explanations
    (Provide the Correct Answer keys and detailed physiological justifications for all 5 questions here at the absolute end of the content document).
    """

    print("Requesting educational content from Gemini Engine...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[book_file, user_prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        )
    )
    
    lesson_content = response.text

    topic_name = "Daily Myofascial Meridian Lesson"
    for line in lesson_content.split("\n"):
        if line.strip() and not line.startswith("#") and "Topic" not in line:
            topic_name = line.strip().replace(":", " -")
            break

    # Manage local UI progression tracking items array
    display_history = completed_lessons.copy()
    display_history.append(f"<b>Active Now:</b> {topic_name}")

    # Process structural layouts into semantic HTML templates
    html_email_content = convert_md_to_styled_html(lesson_content, topic_name, display_history)
    
    # Standardize a very small, short, notification-friendly subject line
    clean_topic_prefix = topic_name.split(" -")[0].split(":")[0].strip()
    subject_header = f"MPT: {clean_topic_prefix[:30]}"

    if args.send:
        # Send using the updated SMTP logic
        send_email(subject_header, html_email_content)

    # Cache archival record values to disk
    os.makedirs("lessons", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    with open(f"lessons/lesson_{today_str}.md", "w", encoding="utf-8") as f:
        f.write(lesson_content)

    # Persist permanent progression telemetry adjustments
    progress["completedLessons"].append(topic_name)
    progress["daysElapsed"] = days_elapsed
    progress["currentPhase"] = current_phase
    with open("progress.json", "w") as f:
        json.dump(progress, f, indent=2)

    client.files.delete(name=book_file.name)
    print("Workflow processing tasks resolved cleanly.")



if __name__ == "__main__":
    main()