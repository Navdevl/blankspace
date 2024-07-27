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

### Deploying the Application on Koyeb

Koyeb is a simple and efficient platform to deploy your applications. Follow these steps to deploy your FastAPI application on Koyeb:

1. **Create a Koyeb Account**:
    - Go to the [Koyeb website](https://www.koyeb.com/) and sign up for an account.

2. **Create a New App**:
    - Once logged in, click on the "Create App" button.
    - Select "GitHub" as the deployment source and connect your GitHub account.
    - Choose the repository containing your FastAPI application.

3. **Configure the Build Settings**:
    - In the "Build Settings" section, select the appropriate branch to deploy.
    - In the "Builder", select "Dockerfile" as the build type.
    - Set the Dockerfile path to:
      ```sh
      ./Dockerfile
      ```

4. **Set Environment Variables**:
    - In the "Environment Variables" section.
    - Add the `SLACK_WEBHOOK_URL` environment variable. You can have it as plain text or secret:
      ```sh
      SLACK_WEBHOOK_URL=YOUR_WEBHOOK_URL
      ```

5. **Deploy the Application**:
    - Click on the "Deploy" button to start the deployment process.
    - Wait for the deployment to complete. You can monitor the progress in the deployment logs.

6. **Verify the Deployment**:
    - Once the deployment is complete, you will be provided with a URL to access your application.
    - Open your browser and navigate to the provided URL to verify that your FastAPI application is running.

For more information on deploying applications with Koyeb, refer to the [Koyeb documentation](https://www.koyeb.com/docs/).


For more information on deploying applications with Fly.io, refer to the [Fly.io documentation](https://fly.io/docs/).
