# 🚀 AI API Service  

A **production-ready AI-powered REST API service** built with **FastAPI** and **Python**, providing endpoints for various AI tasks including **text generation, translation, summarization, and code generation**.  

---

## ✨ Features  
- **Text Generation**: Generate human-like text using advanced AI models  
- **Translation**: Translate text between multiple languages  
- **Summarization**: Condense long texts into concise summaries  
- **Code Generation**: Generate code snippets based on natural language instructions  
- **Multiple AI Providers**: Supports **Groq API** with **Hugging Face fallback**  
- **RESTful API**: Clean, well-documented endpoints  
- **FastAPI Backend**: High-performance asynchronous API  
- **React Frontend**: Modern web interface for testing the API  
- **Production Ready**: Error handling, logging, and health checks  

---

## 🛠️ Tech Stack  

**Backend**  
- Python 3.11+  
- FastAPI  
- Pydantic  
- Uvicorn  
- python-dotenv  

**AI Providers**  
- Groq API (Primary) → *Llama 3.1, Mixtral models*  
- Hugging Face Inference API (Fallback)  

**Frontend**  
- React  
- Axios for API calls  
- Modern CSS styling  

---

## 📦 Installation  

### Prerequisites  
- Python 3.11 or higher  
- Node.js 16+ (for frontend)  
- Groq API account (free at [console.groq.com](https://console.groq.com))  

### 1. Clone the Repository  
```bash
git clone https://github.com/Kaustubh8856/ai-api-service
cd ai-api-service
```

### 2. Set Up Backend  
```bash
# Create virtual environment
python -m venv venv  

# Activate virtual environment
# On Windows:
venv\Scripts\activate  
# On macOS/Linux:
source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables  
Create a **.env** file in the root directory:  

```env
# Groq Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant  

# Hugging Face Configuration (Optional Fallback)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium  

# App Configuration
APP_ENV=development
LOG_LEVEL=INFO
```

### 4. Set Up Frontend  
```bash
# Navigate to frontend directory
cd frontend  

# Install dependencies
npm install  

# Return to root directory
cd ..
```

---

## 🏃 Running the Application  

### Start Backend Server  
```bash
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Development Server  
```bash
# Open new terminal window/tab
cd frontend
npm start
```

### Access the Application  
- **Backend API**: [http://localhost:8000](http://localhost:8000)  
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Frontend Application**: [http://localhost:3000](http://localhost:3000)  

---

## 📚 API Endpoints  

### Core Endpoints  
- `GET /` → Root endpoint with API information  
- `GET /health` → Health check endpoint  
- `GET /info` → API configuration information  

### AI Endpoints  
- `POST /ai/generate` → Generate text from prompt  
- `POST /ai/translate` → Translate text between languages  
- `POST /ai/summarize` → Summarize long text  
- `POST /ai/generate-code` → Generate code from instructions  
- `POST /ai/chat` → Chat completion endpoint  
- `GET /ai/models` → List available AI models  
- `GET /ai/provider` → Get current AI provider information  
- `GET /ai/status` → Service status information  

---

## 🎯 Usage Examples  

### Text Generation  
```bash
curl -X POST "http://localhost:8000/ai/generate"   -H "Content-Type: application/json"   -d '{
    "prompt": "Explain quantum computing in simple terms",
    "max_tokens": 150,
    "temperature": 0.7
  }'
```

### Translation  
```bash
curl -X POST "http://localhost:8000/ai/translate"   -H "Content-Type: application/json"   -d '{
    "text": "Hello, how are you today?",
    "target_language": "Spanish",
    "source_language": "English"
  }'
```

### Code Generation  
```bash
curl -X POST "http://localhost:8000/ai/generate-code"   -H "Content-Type: application/json"   -d '{
    "instruction": "Create a function that checks if a number is prime",
    "language": "python",
    "max_tokens": 100
  }'
```

---

## 🏗️ Project Structure  

```
ai-api-service/
├── app/                    # FastAPI backend
│   ├── routers/            # API route handlers
│   │   └── ai.py           # AI endpoints
│   ├── services/           # AI service integrations
│   │   ├── groq_service.py         # Groq API service
│   │   └── huggingface_service.py  # Hugging Face service
│   ├── models/             # Pydantic models
│   ├── main.py             # FastAPI application
│   └── __init__.py         # Package initialization
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── App.js          # Main App component
│   │   └── App.css         # Styles
│   ├── package.json
│   └── public/
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## 🔧 Configuration  

### Environment Variables  
- **GROQ_API_KEY**: Your Groq API key (**required**)  
- **GROQ_MODEL**: Groq model to use *(default: `llama-3.1-8b-instant`)*  
- **HUGGINGFACE_API_KEY**: Hugging Face API key *(optional fallback)*  
- **HUGGINGFACE_MODEL**: Hugging Face model *(default: `microsoft/DialoGPT-medium`)*  
- **APP_ENV**: Application environment *(development/production)*  
- **LOG_LEVEL**: Logging level *(INFO/DEBUG/ERROR)*  

### Available Models  
- **Groq Models**:  
  - `llama-3.1-8b-instant`  
  - `llama-3.1-70b-versatile`  
  - `mixtral-8x7b-32768`  
  - `gemma-7b-it`  

- **Hugging Face Models**:  
  - `microsoft/DialoGPT-medium`  
  - `facebook/bart-large-cnn`  
  - `google/t5-v1_1-base`  

---

## 🐛 Troubleshooting  

- **ModuleNotFoundError**: Ensure virtual environment is activated and dependencies are installed  
- **API Key Errors**: Verify your Groq API key in the `.env` file  
- **CORS Errors**: Ensure frontend and backend are running on correct ports  
- **Model Not Available**: Check if the specified model exists in your API provider  

---

## 🤝 Contributing  

1. Fork the repository  
2. Create a feature branch  
   ```bash
   git checkout -b feature/amazing-feature
   ```  
3. Commit your changes  
   ```bash
   git commit -m 'Add amazing feature'
   ```  
4. Push to the branch  
   ```bash
   git push origin feature/amazing-feature
   ```  
5. Open a Pull Request  

---

## 📄 License  
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

## 🙏 Acknowledgments  
- [FastAPI](https://fastapi.tiangolo.com/) – Excellent web framework  
- [Groq](https://console.groq.com/) – Fast AI inference provider  
- [Hugging Face](https://huggingface.co/) – Open-source AI models  
- [React](https://react.dev/) – Modern frontend framework  

---

> ⚠️ **Note**: This project is for **demonstration and educational purposes**. Ensure you comply with the **terms of service** of the AI providers you use.  
