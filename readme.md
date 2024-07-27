## Purpose

This repository contains a FastAPI application that listens for incoming Sentry event payloads via a webhook. Upon receiving an event, the application processes the payload to extract relevant information such as project name, environment, message, stacktrace, tags, and browser/OS details. It then formats this information into a structured Slack message and sends a notification to a specified Slack channel. This helps in promptly alerting the team about new errors or issues detected by Sentry.

## How to Run

### Prerequisites

- Python 3.6+
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the FastAPI application**:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

2. **Verify the application is running**:
    Open your browser and navigate to `http://localhost:8000/docs` to see the automatically generated API documentation.

### Configuration

- **SLACK_WEBHOOK_URL**: Update the `SLACK_WEBHOOK_URL` in `main.py` with your actual Slack webhook URL.

### Example Payload

To test the webhook, you can use a tool like `curl` or Postman to send a POST request to `http://localhost:8000/sentry-webhook` with a sample Sentry event payload.

```sh
curl -X POST "http://localhost:8000/sentry-webhook" -H "Content-Type: application/json" -d @sample_payload.json
```

Replace `sample_payload.json` with the path to your JSON file containing the Sentry event payload.

### Notes

- Ensure your FastAPI application is accessible from the internet if you want Sentry to send real event payloads to it.
- You may need to configure your firewall or cloud provider settings to allow traffic on port 8000.