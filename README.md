# 📚 PIXEL MINDS: Personalized AI Tutor for Subject-Specific Q&A Learning

**Track:** Academic Tutor Agent

---

# 📖 Project Overview

**Pixel Minds** is an AI-powered Academic Tutor that helps students learn more effectively using Artificial Intelligence.

The application allows students to upload subject notes in PDF format and provides intelligent learning features such as:

- AI Question Answering
- Summary Generation
- Quiz Generation
- Flashcards
- Personalized Study Plans

The project combines **Frontend Development, Backend Development, PDF Processing, Retrieval-Augmented Generation (RAG), and AI Features** to create an interactive learning experience.

---

# ✨ Features

- 📄 Upload PDF Notes
- 🤖 AI-powered Question Answering
- 📝 Summary Generation
- ❓ Quiz Generation
- 🗂️ Flashcard Generation
- 📅 Personalized Study Plan Generation
- 📚 Subject-Specific Learning

---

# 👥 Team Members

| Team Member | Responsibility |
|-------------|----------------|
| **Nandini Agarwal** | Frontend Development |
| **Mahi Gupta** | Backend Development |
| **Ishita Singh Pundeer** | PDF Processing |
| **Priyanshi** | RAG Development |
| **Kashish Kumari** | AI Features |

---

# 💻 Team Contributions

## 🎨 Frontend Development – Nandini Agarwal

Responsible for:

- Responsive User Interface
- HTML & CSS Development
- Home Page
- Upload PDF Page
- AI Chat Page
- Summary Page
- Quiz Page
- Flashcards Page
- Study Plan Page

---

## ⚙️ Backend Development – Mahi Gupta

Responsible for:

- Backend APIs (FastAPI)
- Connecting Frontend with AI Modules
- Handling Requests & Responses
- Project Integration

---

## 📄 PDF Processing – Ishita Singh Pundeer

Responsible for:

- PDF Upload
- PDF Text Extraction
- Sending Extracted Text to AI Modules

---

## 🧠 RAG Development – Priyanshi

Responsible for:

- Retrieval-Augmented Generation (RAG)
- Context Retrieval
- Improving AI Answer Accuracy

---

## 🤖 AI Features – Kashish Kumari

Implemented using **Python** and **Groq API**.

### AI Features

- Question Answering
- Summary Generation
- Quiz Generation
- Flashcard Generation
- Personalized Study Plan Generation

### Technologies Used

- Python
- Groq API
- python-dotenv

---

# 🛠️ Technologies Used

- Python
- FastAPI & Uvicorn
- Groq API
- HTML
- CSS
- Git
- GitHub
- python-dotenv

---

# 📂 Project Structure

```text
gen-and-agentic-ai-project/
│
├── ai_features/
│   ├── ai_client.py
│   ├── qa.py
│   ├── summary.py
│   ├── quiz.py
│   ├── flashcards.py
│   └── study_plan.py
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/mahigupta-hub/gen-and-agentic-ai-project.git
```

## Move into Project Folder

```bash
cd gen-and-agentic-ai-project
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create .env File

```env
GROQ_API_KEY=YOUR_API_KEY
```

## Run the Project

```bash
uvicorn main:app --reload
```

---

# 🔄 Project Workflow

```text
                 USER
                  │
                  ▼
             Frontend
                  │
                  ▼
              Backend
                  │
      ┌───────────┴─────────────┐
      ▼                         ▼
 PDF Processing             AI Features
      │                         │
      ▼                         │
      RAG ----------------------┘
                  │
                  ▼
             Groq AI
                  │
                  ▼
         Generated Response
                  │
                  ▼
             Frontend
```

---

# 🎯 AI Features

- Answer Questions from Notes
- Generate Summaries
- Generate Quizzes
- Generate Flashcards
- Generate Personalized Study Plans

---

# 🚀 Future Enhancements

- Voice-Based Tutor
- Multi-language Support
- Student Progress Tracking
- Performance Analytics
- Mobile Application

---

# 📄 License

This project is developed for educational purposes as part of a college group project.

---

# 🙏 Acknowledgements

We sincerely thank our faculty members and mentors for their valuable guidance and support throughout the development of **PIXEL MINDS: Personalized AI Tutor for Subject-Specific Q&A Learning**.