# 📚 PIXEL MINDS: Personalized AI Tutor for Subject-Specific Q&A Learning

**Track:** Academic Tutor Agent

---

# 📖 Project Overview

**Pixel Minds** is an AI-powered Academic Tutor that helps students learn more effectively using Artificial Intelligence.

The application allows students to upload subject notes in PDF format and provides intelligent learning features such as Question Answering, Summary Generation, Quiz Generation, Flashcards, and Personalized Study Plans.

The project combines PDF Processing, Retrieval-Augmented Generation (RAG), AI Features, Backend Development, and a responsive Frontend to create an interactive learning experience.

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
| **Priyanshi** | RAG (Retrieval-Augmented Generation) |
| **Kashish Kumari** | AI Features |

---

# 💻 Team Contributions

## 🎨 Frontend Development – Nandini Agarwal

Responsible for:

- Complete UI/UX Design
- Responsive Web Pages
- HTML & CSS Development
- Navigation between pages

Pages Developed:

- Home
- Upload PDF
- AI Chat
- Summary
- Quiz
- Flashcards
- Study Plan

---

## ⚙️ Backend Development – Mahi Gupta

Responsible for:

- Backend APIs
- Connecting Frontend and AI Modules
- Handling Requests and Responses
- Project Integration

---

## 📄 PDF Processing – Ishita Singh Pundeer

Responsible for:

- PDF Upload
- PDF Text Extraction
- Sending Extracted Text to AI Module

---

## 🧠 RAG Development – Priyanshi

Responsible for:

- Retrieval-Augmented Generation
- Retrieving Relevant Context
- Improving Accuracy of AI Responses

---

## 🤖 AI Features – Kashish Kumari

Responsible for implementing the AI-powered features using Python and Google Gemini API.

Implemented:

- ✅ Question Answering
- ✅ Summary Generation
- ✅ Quiz Generation
- ✅ Flashcard Generation
- ✅ Personalized Study Plan
- ✅ Prompt Engineering

Technologies Used:

- Python
- Google Gemini API
- python-dotenv

---

# 🛠️ Technologies Used

- Python
- Google Gemini API
- HTML
- CSS
- Git
- GitHub
- python-dotenv

---

# 📂 Project Structure

```text
PIXEL MINDS
│
├── ai_client.py
├── qa.py
├── summary.py
├── quiz.py
├── flashcards.py
├── study_plan.py
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
git clone https://github.com/yourusername/PIXEL-MINDS.git
```

---

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Create .env File

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run the Project

```bash
python main.py
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
             Gemini AI
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

# 🙏 Acknowledgement

We sincerely thank our faculty members and mentors for their valuable guidance and support throughout the development of **PIXEL MINDS: Personalized AI Tutor for Subject-Specific Q&A Learning**.