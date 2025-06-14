# MediMind Chatbot

A medical chatbot application built with Next.js frontend and Python FastAPI backend, utilizing LangChain and OpenAI for intelligent medical conversations.

## Project Structure

```
medimind-chatbot/
├── frontend/          # Next.js frontend application
└── backend/          # Python FastAPI backend application
```

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- OpenAI API key
- npm or yarn package manager

## Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:3000`

## Running the Application

1. Make sure both backend and frontend servers are running in separate terminal windows
2. Open your browser and navigate to `http://localhost:3000`
3. The application should now be fully functional

## Development

- Frontend development server supports hot reloading
- Backend server supports auto-reload on file changes
- API documentation is available at `http://localhost:8000/docs` when the backend is running

## Technologies Used

### Frontend

- Next.js
- React
- TypeScript
- TailwindCSS
- OpenAI SDK

### Backend

- FastAPI
- LangChain
- ChromaDB
- OpenAI
- Python-dotenv

## Environment Variables

### Backend (.env)

- `OPENAI_API_KEY`: Your OpenAI API key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
