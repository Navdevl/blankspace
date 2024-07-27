## Purpose

This repository contains a FastAPI application that listens for incoming Sentry event payloads via a webhook. Upon receiving an event, the application processes the payload to extract relevant information such as project name, environment, message, stacktrace, tags, and browser/OS details. It then formats this information into a structured Slack message and sends a notification to a specified Slack channel. This helps in promptly alerting the team about new errors or issues detected by Sentry. 

## Disclaimer

This repository contains a simple system that is not production-grade. It is a work in progress and can be improved further. Contributions and suggestions for enhancements are welcome.


## How to Run

### Prerequisites

- Python 3.7+
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

### Creating a Slack Bot and Getting the Webhook URL

To send notifications to Slack, you need to create a Slack bot and obtain a webhook URL. Follow these steps:

1. **Create a Slack App**:
    - Go to the [Slack API: Applications](https://api.slack.com/apps) page.
    - Click on the "Create New App" button.
    - Choose "From scratch".
    - Enter an app name and select the Slack workspace where you want to install the app.
    - Click "Create App".

2. **Add Incoming Webhooks**:
    - In the left sidebar, click on "Incoming Webhooks".
    - Toggle the "Activate Incoming Webhooks" switch to "On".
    - Click on the "Add New Webhook to Workspace" button.
    - Select the channel where you want the bot to post messages and click "Allow".
    - Copy the generated webhook URL. This is your `SLACK_WEBHOOK_URL`.

3. **Update the .env File**:
    - Open the `.env` file in your project directory.
    - Add the following line, replacing `YOUR_WEBHOOK_URL` with the URL you copied:
      ```sh
      SLACK_WEBHOOK_URL=YOUR_WEBHOOK_URL
      ```

### Example Payload

To test the webhook, you can use a tool like `curl` or Postman to send a POST request to `http://localhost:8000/sentry-webhook` with a sample Sentry event payload.

```sh
curl -X POST "http://localhost:8000/sentry-webhook" -H "Content-Type: application/json" -d @samples/alert.json
```

#### Deploying to Fly.io

Fly.io is a platform for running full-stack apps and databases close to your users. Follow these steps to deploy your FastAPI application to Fly.io:

1. **Install Flyctl**:
    Flyctl is the command-line tool for interacting with Fly.io. You can install it using the following command:
    ```sh
    curl -L https://fly.io/install.sh | sh
    ```

2. **Sign in to Fly.io**:
    If you don't have a Fly.io account, you can sign up for one. Then, sign in using Flyctl:
    ```sh
    flyctl auth login
    ```

3. **Create and configure a new Fly.io application**:
    Initialize a new Fly.io application in your project directory:
    ```sh
    flyctl launch
    ```
    Follow the prompts to set up your application. This will create a `fly.toml` configuration file in your project directory.

4. **Set environment variables**:
    You need to set the `SLACK_WEBHOOK_URL` environment variable in Fly.io. You can do this using the following command:
    ```sh
    flyctl secrets set SLACK_WEBHOOK_URL=YOUR_WEBHOOK_URL
    ```

5. **Deploy your application**:
    Deploy your FastAPI application to Fly.io using the following command:
    ```sh
    flyctl deploy
    ```

6. **Access your deployed application**:
    Once the deployment is complete, Fly.io will provide you with a URL where your application is accessible. You can visit this URL in your browser to see your running application.

For more information on deploying applications with Fly.io, refer to the [Fly.io documentation](https://fly.io/docs/).
