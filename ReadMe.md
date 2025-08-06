Virtual Banking Assistant
This project is a web-based chat application that connects to a powerful backend AI agent hosted on IBM Watsonx. It allows users to ask banking-related questions and receive instant, intelligent responses.

The project is divided into two main parts:

Backend: A Python server built with Flask that handles authentication with IBM Cloud and acts as a secure intermediary between the frontend and the AI agent.

Frontend: A clean, modern chat interface built with HTML, CSS (Tailwind), and vanilla JavaScript that users interact with.

Project Structure
Bank_Agent/
├── backend/
│   ├── venv/                 # (Will be created during setup)
│   ├── agent.py              # The Flask server logic
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # (Will be created during setup)
│
├── frontend/
│   └── index.html            # The chat interface
│
└── README.md                 # Setup and project information

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python (Version 3.8 or newer is recommended)

Git (for cloning the project)

Setup Instructions
Follow these steps carefully to get the project running on your local machine.

1. Clone the Repository
First, clone the project from its source repository to your local machine. Open your terminal or command prompt and run:

git clone <your-repository-url>
cd Bank_Agent

(Note: Replace <your-repository-url> with the actual URL of your Git repository.)

2. Set Up the Backend
The backend requires a few steps to configure its environment and dependencies.

a. Navigate to the backend directory:

cd backend

b. Create and activate a virtual environment:
This creates an isolated environment for the project's Python packages, which is a standard best practice.

On Windows:

python -m venv venv
.\venv\Scripts\activate

On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Your terminal prompt should now show (venv) at the beginning.

c. Install Python dependencies:

pip install -r requirements.txt

d. Create the environment variables file:
Create a new file named .env inside the backend folder. This file will store your secret credentials. Add the following content to it:

API_KEY="your-real-ibm-cloud-api-key"
AGENT_ENDPOINT="your-watsonx-agent-deployment-url"

Important: Replace the placeholder text with your actual IBM Cloud API Key and your Watsonx Agent's deployment URL.

3. Running the Application
To run the application, you need to start both the backend server and the frontend interface.

a. Start the Backend Server:
Make sure you are in the backend directory and your virtual environment is activated. Then, run the following command:

python agent.py

The server will start, and you should see output indicating it's running on http://127.0.0.1:5000. Keep this terminal window open.

b. Launch the Frontend:
Open a new terminal or use your computer's file explorer to navigate to the frontend directory. Double-click the index.html file. This will open the chat application in your default web browser.

You can now start chatting with your virtual banking assistant!
# thank you