const API_URL = "https://gen-and-agentic-ai-project.onrender.com"; 

// Global "+ New Chat" Button Handler
document.addEventListener("DOMContentLoaded", () => {
    const newChatBtn = document.querySelector(".new-chat");

    if (newChatBtn) {
        newChatBtn.addEventListener("click", () => {
            // 1. Clear saved PDF data and session state to start fresh
            localStorage.removeItem("uploaded_pdf_name");
            localStorage.removeItem("extracted_pdf_text");

            // 2. Redirect to the home page so the user can upload a new PDF
            window.location.href = "index.html";
        });
    }
});