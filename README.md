# SecureText - Cryptography Learning Platform

A web-based application for learning and implementing AES-256, RSA-2048, and SHA-256 cryptographic algorithms with interactive visualizations.

## Features

- **AES-256 Encryption/Decryption**: Symmetric encryption with visual step-by-step process
- **RSA-2048 Encryption/Decryption**: Asymmetric encryption with key generation visualization
- **SHA-256 Hashing**: One-way hashing function
- **Interactive Learning Mode**: See exactly how encryption algorithms work
- **History Tracking**: Keep track of all cryptographic operations
- **User Authentication**: Secure login system with JWT

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SecureText.git
cd SecureText
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Run the backend server:
```bash
uvicorn backend.main:app --reload
```

5. Open `frontend/index.html` in your browser or use a local server:
```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080
# Then open http://localhost:8080
```

## Live Demo

Visit: [https://securetext.mayankmangipudi.me](https://securetext.mayankmangipudi.me)

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy
- Cryptography library
- PyCryptodome
- JWT Authentication

**Frontend:**
- HTML5
- TailwindCSS
- Alpine.js
- Vanilla JavaScript


## Author

**Mayank M (22BCE3115)**

## License

MIT License - feel free to use for educational purposes.
