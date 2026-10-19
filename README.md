# 🏥 MediSync — Smart Healthcare Management System

<p align="center">
  <strong>A modern healthcare management web application built with Django.</strong>
  <br>
  Manage medicines, appointments, and medical records through one organized platform.
</p>

<p align="center">
  <a href="https://medisync-pnz0.onrender.com">🌐 Live Demo</a>
  &nbsp; • &nbsp;
  <a href="#-features">Features</a>
  &nbsp; • &nbsp;
  <a href="#-installation">Installation</a>
</p>

---

## 📌 About the Project

**MediSync** is a healthcare management web application designed to help users organize essential healthcare information in one place.

The application provides a dashboard for viewing healthcare activities, managing medicines, scheduling appointments, and maintaining medical records. It also includes an AI Health Assistant interface designed to help users explore health-related questions.

The project focuses on creating a user-friendly, organized, and accessible healthcare management experience using Django.

## ✨ Features

* 🔐 **User Authentication** — Register, log in, and access protected pages.
* 📊 **Dashboard** — View an overview of medicines, appointments, and medical records.
* 💊 **Medicine Management** — Add, view, edit, and delete medicine information.
* 📅 **Appointment Management** — Organize doctor appointments and appointment details.
* 🩺 **Medical Records** — Maintain and manage medical record entries.
* 🤖 **AI Health Assistant** — Interact with an AI-powered assistant through the application's chat interface.
* 💬 **Conversation Management** — Access and manage supported chat conversations.
* 👤 **User Profile** — View account information.
* 📱 **Responsive Interface** — Designed to support different screen sizes.
* ☁️ **Web Deployment** — Hosted online using Render.

## 🛠️ Technologies Used

| Technology        | Purpose                                 |
| ----------------- | --------------------------------------- |
| Python            | Backend programming                     |
| Django            | Web application framework               |
| HTML5             | Page structure                          |
| CSS3              | Styling and responsive design           |
| JavaScript        | Client-side interactions                |
| SQLite            | Local development database              |
| PostgreSQL        | Production database, when configured    |
| Google Gemini API | AI assistant integration                |
| Git and GitHub    | Version control and source code hosting |
| Render            | Web application deployment              |

## 🖥️ Application Modules

### 1. Dashboard

Provides an overview of the user's healthcare activities.

### 2. Medicines

Allows users to manage medicine details, dosage information, instructions, and reminders.

### 3. Appointments

Helps users organize doctor appointments, including doctor names, hospitals, dates, times, and notes.

### 4. Medical Records

Provides a place to store and manage medical record entries.

### 5. AI Health Assistant

Provides a chat interface for AI-powered health-related assistance when the API is configured.

### 6. User Profile

Displays account information for the authenticated user.

## 🌐 Live Demo

**Visit MediSync:**

https://medisync-pnz0.onrender.com

> Note: The live application may take some time to start if the hosting service has been idle.

## ⚙️ Installation

Follow these steps to run MediSync on your local machine.

### Prerequisites

Install the following:

* Python
* Git
* Visual Studio Code (recommended)

### Step 1: Clone the repository

```bash
git clone https://github.com/gaganamg16/MediSync.git
```

### Step 2: Open the project directory

```bash
cd MediSync
```

### Step 3: Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
```

### Step 4: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the Command Prompt activation command instead:

```cmd
venv\Scripts\activate.bat
```

### Step 5: Install dependencies

If the project contains `requirements.txt`, run:

```powershell
python -m pip install -r requirements.txt
```

### Step 6: Configure environment variables

Configure the required environment variables in your local environment or your project's supported environment configuration.

For local development, ensure Django's secret key and debug settings are configured appropriately.

If the AI Health Assistant requires a Gemini API key, configure:

```text
GEMINI_API_KEY=your_gemini_api_key
```

**Security:** Never commit API keys, passwords, database credentials, or your production Django secret key to GitHub.

### Step 7: Apply database migrations

```powershell
python manage.py migrate
```

### Step 8: Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create the account.

### Step 9: Start the development server

```powershell
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## 📂 Project Structure

The project uses Django apps to organize different areas of functionality. The structure below is illustrative; individual filenames may differ.

```text
MediSync/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── templates/
│   └── views.py
│
├── medicines/
│   ├── templates/
│   ├── models.py
│   └── views.py
│
├── appointments/
│   ├── templates/
│   ├── models.py
│   └── views.py
│
├── records/
│   ├── templates/
│   ├── models.py
│   └── views.py
│
├── ai_assistant/
│   ├── templates/
│   └── views.py
│
├── static/
│   └── medisync/
│       ├── css/
│       └── js/
│
├── manage.py
├── requirements.txt
└── README.md
```

## 🔒 Security and Privacy

* Keep API keys and secret credentials outside source control.
* Use environment variables for production configuration.
* Disable Django debug mode in production.
* Configure allowed hosts and database credentials securely.
* Avoid entering unnecessary sensitive medical information into an AI assistant.
* Verify important healthcare decisions with a qualified healthcare professional.

MediSync is a software project for healthcare information management and is not a substitute for professional medical diagnosis or treatment.

## 🚀 Future Improvements

Potential improvements include:

* 🎨 Further enhancements to the dashboard and application design.
* ⏰ Medicine reminder notifications.
* 📧 Appointment reminder emails.
* 📈 Healthcare activity charts and summaries.
* 📄 Medical record export and download.
* 🔐 Additional security and privacy improvements.
* 📱 Enhanced mobile experience.
* 🧪 Automated testing and improved test coverage.

## 👩‍💻 Developer

**Gagana M G**

Computer Science and Engineering Student

GitHub: [@gaganamg16](https://github.com/gaganamg16)

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!

---

<p align="center">
  Built with ❤️ using Python and Django.
</p>
