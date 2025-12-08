# Online Coding Interview Platform

A real-time collaborative coding platform with code execution capabilities.

## Prerequisites
- Python 3.8+
- Node.js v20+
- npm

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd 02_code_itws
   ```

2. **Backend Setup**:
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install django djangorestframework django-cors-headers

   # Run migrations
   python backend/manage.py migrate
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

You can run both the backend and frontend servers with a single command:

```bash
npm run dev
```

This will start:
- Backend on `http://localhost:8003`
- Frontend on `http://localhost:5173`

Alternatively, you can run them separately:

1. **Start Backend**:
   ```bash
   source .venv/bin/activate
   python backend/manage.py runserver 8003
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

## Testing

### Integration Tests (E2E)
We use Playwright for end-to-end testing.

1. Ensure the backend is running on port 8003.
2. Run the tests:
   ```bash
   cd frontend
   npx playwright test
   ```

   To see the test report:
   ```bash
   npx playwright show-report
   ```

## Docker Support

You can run the entire application (Frontend + Backend) in a single Docker container.

1. **Build the image**:
   ```bash
   docker build -t code-itws .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 code-itws
   ```

   Access the application at `http://localhost:8000`.

## Features
- **Real-time Collaboration**: Code changes are synced instantly between users in the same room.
- **Client-Side Execution**: Code runs securely in your browser using WebAssembly (Pyodide for Python).
- **Multi-Language Support**: Python and JavaScript.
- **Modern Editor**: Powered by CodeMirror 6 with syntax highlighting.

## Tech Stack
- **Frontend**: React, Vite, CodeMirror 6, Pyodide (WASM)
- **Backend**: Django, Django Channels (WebSockets), Daphne
- **Testing**: Playwright
- **DevOps**: Docker (Multi-stage build)
