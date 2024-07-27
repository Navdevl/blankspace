import os
import json
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()
load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def format_stacktrace(stacktrace):
    if not stacktrace or 'frames' not in stacktrace:
        return "No stacktrace available"
    
    formatted = []
    for frame in reversed(stacktrace['frames'][-5:]):  # Show last 5 frames
        filename = frame.get('filename', 'Unknown file')
        lineno = frame.get('lineno', '?')
        function = frame.get('function', 'Unknown function')
        formatted.append(f"{filename}:{lineno} in {function}")
    
    return "\n".join(formatted)

def extract_stacktrace(event):
    """
    Extracts and formats the stacktrace from the event.
    """
    stacktrace = event.get('stacktrace')
    if not stacktrace:
        exception = event.get('exception', {})
        values = exception.get('values', [])
        if values:
            stacktrace = values[0].get('stacktrace')
    
    return format_stacktrace(stacktrace) if stacktrace else "No stacktrace available"

def extract_tags(event):
    """
    Extracts and formats the tags from the event.
    """
    tags = event.get('tags', [])
    return "\n".join([f"• {tag[0]}: {tag[1]}" for tag in tags])

def extract_browser_os_info(event):
    """
    Extracts browser and OS information from the event.
    """
    contexts = event.get('contexts', {})
    browser = contexts.get('browser', {})
    os = contexts.get('client_os', {})
    browser_info = f"{browser.get('name', 'Unknown')} {browser.get('version', '')}"
    os_info = f"{os.get('name', 'Unknown')} {os.get('version', '')}"
    return browser_info, os_info

def build_slack_message(event, project, environment, date_time, message, stacktrace, tag_string, browser_info, os_info, url):
    """
    Constructs the Slack message payload.
    """
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 New {event.get('level', 'error').upper()} in {project}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Environment:*\n{environment}"},
                    {"type": "mrkdwn", "text": f"*Time:*\n{date_time}"},
                    {"type": "mrkdwn", "text": f"*Browser:*\n{browser_info}"},
                    {"type": "mrkdwn", "text": f"*OS:*\n{os_info}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Message:*\n```{message}```"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Stacktrace:*\n```{stacktrace}```"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Tags:*\n{tag_string}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View in Sentry"
                        },
                        "url": url,
                        "style": "primary"
                    }
                ]
            }
        ]
    }

@app.post("/sentry-webhook")
async def sentry_webhook(request: Request):
    payload = await request.json()
    event = payload['event']
    
    project = payload.get('project_name', 'Unknown Project')
    environment = event.get('environment', 'Unknown')
    message = event.get('logentry', {}).get('formatted') or event.get('title')
    url = payload.get('url', '#')
    triggering_rules = payload.get('triggering_rules', [])
    
    if triggering_rules:
        message = f"{message} (Triggered by: {', '.join(triggering_rules)})"
    
    timestamp = event.get('timestamp')
    date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown time'

    # Extract stacktrace
    stacktrace = extract_stacktrace(event)

    # Extract tags
    tag_string = extract_tags(event)

    # Extract browser and OS info
    browser_info, os_info = extract_browser_os_info(event)

    # Construct the Slack message
    slack_message = build_slack_message(event, project, environment, date_time, message, stacktrace, tag_string, browser_info, os_info, url)

    # Send the message to Slack
    response = requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps(slack_message),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return {"message": "Slack notification sent successfully"}
    else:
        return {"error": f"Failed to send Slack notification. Status code: {response.status_code}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)