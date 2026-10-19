# 🏥 MediSync — Smart Healthcare Management System

MediSync is a web-based healthcare management application built with Django. It helps users organize their health-related information, manage appointments, track medicines, and access AI-powered health information through an integrated chatbot.

### ✨ Features

* 🔐 **User Authentication** — Register, log in, and securely access your account.
* 📊 **Dashboard** — View a summary of medicines, appointments, and medical records.
* 💊 **Medicine Management** — Add, view, edit, and delete medicine information.
* 📅 **Appointment Management** — Organize doctor appointments and maintain appointment details.
* 🩺 **Medical Records** — Store and manage health-related records.
* 🤖 **AI Health Assistant** — Ask general health-information questions using Google's Gemini AI.
* 💬 **Chat History** — Save and revisit previous AI assistant conversations.
* 🗑️ **Conversation Management** — Delete individual chatbot conversations.
* 👤 **User Profile** — View account information.

### 🛠️ Technologies Used

| Technology        | Purpose                               |
| ----------------- | ------------------------------------- |
| Python            | Backend programming                   |
| Django            | Web application framework             |
| SQLite            | Database                              |
| HTML5             | Web page structure                    |
| CSS3              | Styling and responsive layouts        |
| JavaScript        | Interactive frontend features         |
| Google Gemini API | AI-powered health-information chatbot |
| Git and GitHub    | Version control and project hosting   |

### 📂 Project Structure

```text
MediSync/
├── accounts/
├── appointments/
├── medicines/
├── records/
├── ai_assistant/
├── config/
├── templates/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

*The actual folder structure may vary depending on the current project configuration.*

## ⚙️ Installation and Setup

### Prerequisites

* Python installed
* Git installed
* A Google Gemini API key for the AI assistant

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Navigate to the project folder

```bash
cd MediSync
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own key. Never commit the `.env` file or expose your API key publicly.

Ensure your application loads the environment variables using the configuration already implemented in the project.

### 7. Apply database migrations

```bash
python manage.py migrate
```

### 8. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## 🤖 AI Health Assistant

MediSync integrates Google's Gemini API to provide general health information through a conversational interface.

The assistant is designed to provide educational information, not medical diagnoses or prescriptions. Users should consult qualified healthcare professionals for personal medical concerns.

## 🔒 Security and Privacy

* Keep API keys and other secrets in environment variables.
* Do not upload `.env`, virtual environments, or local database files to GitHub.
* Protect user accounts and personal information.
* Do not use real patient information in development or demonstration environments.

## 🚧 Future Improvements

* Conversation-aware AI responses.
* Medicine reminder notifications.
* Improved mobile responsiveness.
* Additional dashboard analytics.
* Deployment to a production hosting platform.
* Enhanced privacy and security controls.

## 🎓 Project Information

**Project Name:** MediSync
**Project Type:** Healthcare Management Web Application
**Backend:** Django and Python
**AI Integration:** Google Gemini API

## 👩‍💻 Author

Developed as a software development project to explore web development, healthcare management, and AI integration.

---

⭐ If you find this project interesting, consider starring the repository!!
