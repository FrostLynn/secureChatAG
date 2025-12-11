# SecureChat AG

A secure, end-to-end encrypted (E2EE) real-time chat application built with React and FastAPI.

## Features

*   **End-to-End Encryption**: Messages are encrypted on the client side using ChaCha20 (text) and AES-GCM (files) before being sent to the server. The server *never* sees plaintext.
*   **Real-Time Messaging**: Powered by WebSockets for instant delivery.
*   **Google Authentication**: Secure login via Google OAuth.
*   **Media Support**: Send and receive images, videos, and audio files with inline previews.
*   **Group Chats**: Create and manage secure group conversations.
*   **Message Persistence**: Encrypted messages are stored safely in an SQLite database.

## Architecture

*   **Frontend**: React, Vite, TailwindCSS
*   **Backend**: Python, FastAPI, SQLModel (SQLite)
*   **Cryptography**: 
    *   Text: ChaCha20-Poly1305 (via `libsodium-wrappers`)
    *   Files: AES-GCM (via `crypto-js`)
    *   Key Derivation: PBKDF2

## Setup & Installation

### Prerequisites
*   Node.js (v18+)
*   Python (v3.10+)

### Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment Variables:
    *   Create a `.env` file in the `backend` folder.
    *   Add your Google OAuth credentials and a generic secret key (for session signing, not message encryption):
        ```env
        SECRET_KEY=your_session_secret_key
        GOOGLE_CLIENT_ID=your_google_client_id
        GOOGLE_CLIENT_SECRET=your_google_client_secret
        ```
5.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will run on `http://localhost:8000`.

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The app will run on `http://localhost:5173` (or similar).

## Usage

1.  Open the frontend in your browser.
2.  Log in with your Google account.
3.  Set a username if prompted.
4.  Enter a **Secret Key** in the sidebar. 
    *   **Important**: To chat with another user, both MUST use the SAME Secret Key for this demo version. (In a full production app, this would be replaced by Public/Private key exchange like Signal/WhatsApp).
5.  Search for a user by their username to start a chat.
6.  Send messages or attach files.

## Deployment with Docker

You can easily deploy the entire stack using Docker Compose.

### Prerequisites
*   Docker and Docker Compose installed on your machine.

### Steps
1.  Ensure your `backend/.env` file is configured (see Backend Setup step 4).
2.  Run the following command in the root directory:
    ```bash
    docker-compose up --build -d
    ```
3.  Access the application:
    *   **Frontend**: `http://localhost:3001`
    *   **Backend API**: `http://localhost:8000`

### Troubleshooting
*   If you change code, remember to rebuild: `docker-compose up --build -d`.
*   If the database isn't saving, ensure permissions on `database.db` are correct if mounted.

## Security Note

This project is a demonstration of E2EE principles.
- **Server Knowledge**: The server stores only `cipher` blob and `nonce`. It cannot decrypt messages.
- **Key Management**: Currently uses a shared-secret model ("Room Key") for simplicity in demonstration. Ensure all participants verify they are using the correct shared key.
