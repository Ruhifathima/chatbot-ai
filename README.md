*TO CLONE THE REPOSITORY:*
git clone https://github.com/Ruhifathima/chatbot-ai.git
cd chatbot-ai

*TO SET UP BACKEND:*
cd backend

python -m venv venv

venv\Scripts\activate 

pip install -r requirements.txt

GEMINI_API_KEY=your-key-here

uvicorn main:app --reload


*TO SET UP FRONTEND:*
cd ../frontend

npm install

npm start

