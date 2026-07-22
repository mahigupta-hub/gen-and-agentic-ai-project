// Automatically switch between Localhost and Render
const API_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://127.0.0.1:8000"
    : "https://gen-and-agentic-ai-project.onrender.com";

// Global "+ New Chat" Button Handler
document.addEventListener("DOMContentLoaded", () => {
    const newChatBtn = document.querySelector(".new-chat");

    if (newChatBtn) {
        newChatBtn.addEventListener("click", () => {
            // 1. Clear saved PDF data and session state to start fresh
            localStorage.removeItem("uploaded_pdf_name");
            localStorage.removeItem("extracted_pdf_text");

            // 2. Redirect to the home page so the user can upload a new PDF
            window.location.href = "upload.html";
        });
    }
});

// Global PDF File Name Display
document.addEventListener("DOMContentLoaded", () => {
    const fileNameDisplay = document.getElementById("pdf-filename");
    
    if (fileNameDisplay) {
        // Get the actual file name saved during upload
        const savedName = localStorage.getItem("uploaded_pdf_name");
        
        // Display the name, or a fallback if they haven't uploaded anything
        fileNameDisplay.textContent = savedName ? `📄 ${savedName}` : "📄 No file uploaded";
    }
});