# 🛡️ SAFE-SPHERE

**Empowering Communities, Ensuring Safety, Inspiring Change**

---

## 🚀 Technology Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37B24D?style=for-the-badge&logo=celery&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)

### AI & Authentication
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=langchain&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![ChromaDB](https://img.shields.io/badge/ChromaDB-00A3FF?style=for-the-badge)
![Clerk](https://img.shields.io/badge/Clerk-6C47FF?style=for-the-badge&logo=clerk&logoColor=white)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Safe-Sphere** is an open-source community safety platform that integrates a **FastAPI** backend with a **React + Vite** frontend to deliver:

- 🚨 **Real-time Emergency Reporting** - Instant SOS alerts and emergency location sharing
- 📍 **Geospatial Crime Mapping** - Interactive maps showing police stations and crime hotspots
- 📋 **Multi-type FIR Registration** - Lost items, cyber crimes, sexual assault cases, theft reports, and more
- 🤖 **AI-Powered Chatbot** - RAG-based legal guidance and safety information assistant
- 🔐 **Secure Authentication** - Clerk-based JWT authentication with role-based access control
- 📊 **Crime Data Analytics** - Search and analyze historical crime patterns

Designed for developers and safety organizations, Safe-Sphere offers a scalable, modular, and production-ready architecture.

---

## ✨ Key Features

### Backend Capabilities

| Feature | Description | Technology |
|---------|-------------|------------|
| **FIR Management** | Register multiple types of incidents (lost items, cyber crimes, sexual assault, theft, missing persons) | FastAPI + SQLAlchemy |
| **User Profiles** | Secure user registration, authentication, and profile management | Clerk JWT + PostgreSQL |
| **SOS Assistance** | Real-time emergency response with nearest police station finder | GeoPy + In-memory Caching |
| **Crime Search** | Query and filter crime data with advanced filters | PostgreSQL + SQLAlchemy |
| **AI Chatbot** | RAG-powered assistant using Mistral LLM and HuggingFace embeddings | LangChain + ChromaDB + Celery |
| **Async Processing** | Background task execution for AI responses and heavy computations | Celery + Redis |

### Frontend Capabilities

| Feature | Description | Technology |
|---------|-------------|------------|
| **Responsive UI** | Mobile-first design with smooth animations | React + TailwindCSS |
| **Interactive Maps** | Real-time geospatial visualization | Leaflet + Mapbox GL |
| **Data Visualization** | Crime statistics and dashboard charts | Chart.js + React-ChartJS-2 |
| **Forms & Validation** | Multi-step incident reporting forms | React + Axios |
| **Dark Mode Support** | Customizable theme with TailwindCSS | TailwindCSS Animate |

---

## 🏗️ Project Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        React Client                         │
│              (Vite + React 18 + TailwindCSS)               │
└────────────────────┬────────────────────────────────────────┘
                     │ (HTTP/REST)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Routes: FIR | Profile | SOS | Bot | Search          │  │
│  └────────────────┬──────────────────┬─────────────────┘  │
│                   ▼                  ▼                      │
│  ┌────────────────────────┐  ┌──────────────────────┐     │
│  │  Service Layer         │  │  Celery Workers      │     │
│  │  - FIRService          │  │  - AI Task Handler   │     │
│  │  - UserService         │  └──────────────────────┘     │
│  │  - SOSService          │           │                    │
│  │  - CrimeService        │           ▼                    │
│  └────────────┬───────────┘  ┌──────────────────────┐     │
│               ▼               │  LangChain RAG       │     │
│  ┌────────────────────────┐  │  - ChromaDB          │     │
│  │ Repository Layer       │  │  - HuggingFace LLM   │     │
│  │ - FIRRepository        │  │  - Mistral Model     │     │
│  │ - UserRepository       │  └──────────────────────┘     │
│  │ - CrimeRepository      │                                │
│  └────────────┬───────────┘                                │
│               ▼                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │         SQLAlchemy Models                          │   │
│  │  (User, FIR types, CrimeData, Incidents)           │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
           ▲                        ▲                ▲
           │ (SQL)                  │ (Broker)       │
    ┌──────────────┐        ┌───────────────┐ ┌──────────┐
    │  PostgreSQL  │        │  Redis Cache  │ │ Clerk    │
    │  (Database)  │        │  (Task Queue) │ │ (Auth)   │
    └──────────────┘        └───────────────┘ └──────────┘
```

### MVC Architecture

**Controllers (Routes):** `/server/app/api/routes/`
- `bot.py` - AI chatbot endpoints
- `fir.py` - FIR registration endpoints
- `profile.py` - User profile management
- `sos.py` - Emergency services
- `search.py` - Crime data search

**Services:** `/server/app/services/`
- Business logic orchestration
- Multi-layer data processing
- In-memory caching for performance

**Repositories:** `/server/app/repositories/`
- Data access abstraction
- SQLAlchemy query encapsulation
- CRUD operations

**Models:** `/server/app/models/`
- SQLAlchemy ORM definitions
- Database schema

---

## 📁 Directory Structure

```
safe-sphere/
├── client/                          # React Frontend (Vite)
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   ├── pages/                   # Page components
│   │   ├── hooks/                   # Custom React hooks
│   │   ├── services/                # API service clients
│   │   ├── context/                 # React context for state
│   │   ├── styles/                  # Global styles
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── server/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/              # API endpoint handlers
│   │   │   │   ├── bot.py
│   │   │   │   ├── fir.py
│   │   │   │   ├── profile.py
│   │   │   │   ├── sos.py
│   │   │   │   └── search.py
│   │   │   └── dependencies/        # Shared dependencies
│   │   ├── services/                # Business logic layer
│   │   ├── repositories/            # Data access layer
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── bot/                     # AI RAG subsystem
│   │   │   ├── retrieval.py
│   │   │   ├── rag_chain.py
│   │   │   └── vector_store.py
│   │   ├── core/
│   │   │   └── config.py            # Configuration & settings
│   │   ├── utils/
│   │   │   ├── celery_app.py
│   │   │   ├── errors.py
│   │   │   └── date_utils.py
│   │   ├── main.py                  # FastAPI app initialization
│   │   └── models/
│   │       └── database.py          # Database connection
│   ├── run.py                       # Application entry point
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md                    # Backend documentation
│
├── README.md                        # This file
└── .gitignore

```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js** 18.x or higher (for frontend)
- **Python** 3.10 or higher (for backend)
- **PostgreSQL** 13+ (database)
- **Redis** 6+ (task queue & caching)
- **npm** or **yarn** (package manager)
- **pip** (Python package manager)

### Backend Setup

1. **Navigate to server directory:**
   ```bash
   cd server
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
   
   Required environment variables:
   - `DATABASE_URL` - PostgreSQL connection string
   - `REDIS_URL` - Redis connection URL
   - `CLERK_SECRET_KEY` - Clerk authentication secret
   - `HUGGINGFACE_API_KEY` - HuggingFace API key
   - `FRONTEND_URL` - React frontend URL (for CORS)

5. **Initialize the database:**
   ```bash
   flask db upgrade
   # Or if using Alembic:
   alembic upgrade head
   ```

6. **Start Celery worker (in separate terminal):**
   ```bash
   celery -A app.utils.celery_app worker --loglevel=info
   ```

7. **Run the FastAPI server:**
   ```bash
   python run.py
   # Server runs on http://localhost:5000
   ```

### Frontend Setup

1. **Navigate to client directory:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env.local
   ```
   
   Required environment variables:
   - `VITE_API_URL` - Backend API URL (http://localhost:5000)
   - `VITE_CLERK_PUBLISHABLE_KEY` - Clerk publishable key
   - `VITE_MAPBOX_TOKEN` - Mapbox GL token (optional)

4. **Start development server:**
   ```bash
   npm run dev
   # Frontend runs on http://localhost:5173
   ```

### Running the Application

1. **Start PostgreSQL and Redis:**
   ```bash
   # PostgreSQL (if running locally)
   pg_ctl start
   
   # Redis (if running locally)
   redis-server
   ```

2. **Start backend (Terminal 1):**
   ```bash
   cd server
   source venv/bin/activate
   python run.py
   ```

3. **Start Celery worker (Terminal 2):**
   ```bash
   cd server
   source venv/bin/activate
   celery -A app.utils.celery_app worker --loglevel=info
   ```

4. **Start frontend (Terminal 3):**
   ```bash
   cd client
   npm run dev
   ```

5. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000
   - API Docs: http://localhost:5000/docs (Swagger UI)

---

## 📚 API Documentation

### Core Endpoints

#### Authentication
- **POST** `/api/profile/register` - User registration
- **GET** `/api/profile/me` - Get current user profile
- **GET** `/api/profile/check` - Check authentication status

#### FIR Management
- **POST** `/api/fir/lost-item` - Register lost item
- **POST** `/api/fir/cyber-crime` - Report cyber crime
- **POST** `/api/fir/rape-case` - Report sexual assault
- **POST** `/api/fir/theft-efir` - Register theft
- **POST** `/api/fir/missing-person` - Report missing person
- **GET** `/api/profile/my-firs` - Get user's FIR reports

#### SOS & Emergency
- **GET** `/api/sos/nearest-police-stations` - Find nearest police stations
- **GET** `/api/sos/crime-data` - Get area crime statistics
- **GET** `/api/sos/crime-data/{area}` - Get crime data by area

#### AI Chatbot
- **POST** `/api/bot/generate` - Generate AI response
- **GET** `/api/bot/status/{task_id}` - Get AI response status

#### Search
- **GET** `/api/search/search` - Search crime database

### Full API Documentation

Visit **http://localhost:5000/docs** when the server is running for interactive Swagger UI documentation.

---

## 🔐 Environment Variables

### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/safe_sphere

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key

# AI/LLM
HUGGINGFACE_API_KEY=your_huggingface_api_key
MISTRAL_MODEL_ID=mistralai/Mistral-Nemo-2407-12B

# Application
FRONTEND_URL=http://localhost:5173
DEBUG=False
```

### Frontend (`.env.local`)

```env
VITE_API_URL=http://localhost:5000
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
VITE_MAPBOX_TOKEN=your_mapbox_token
```

---

## 🛠️ Language Composition

- **JavaScript**: 89% (React + Vite frontend)
- **Python**: 9.5% (FastAPI backend)
- **CSS**: 1.1% (TailwindCSS styling)
- **Other**: 0.4%

---

## 🧪 Testing

### Backend Testing

```bash
cd server
pytest tests/
pytest tests/ -v  # Verbose output
pytest tests/ --cov=app  # With coverage
```

### Frontend Testing

```bash
cd client
npm run test
npm run test:coverage
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests for new features
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

---

## 📖 Documentation

- **[Backend Architecture](./server/README.md)** - Detailed backend design and implementation
- **[API Reference](http://localhost:5000/docs)** - Interactive API documentation (when server is running)

---

## 🔒 Security

- **JWT Authentication** via Clerk
- **Role-Based Access Control** on protected endpoints
- **Input Validation** using Pydantic schemas
- **SQL Injection Prevention** via SQLAlchemy ORM
- **CORS Protection** for frontend-backend communication
- **Secure Password Storage** with bcrypt hashing

---

## 📊 Performance Features

- **Async Request Handling** with FastAPI
- **Background Task Processing** with Celery + Redis
- **In-Memory Geospatial Caching** for SOS services
- **Vector Database Caching** for RAG embeddings
- **Optimized Database Queries** with indexes
- **Frontend Code Splitting** with Vite

---

## 🐛 Known Issues & Roadmap

### Current Limitations
- RAG chain initialization can be slow on first run
- Vector store requires periodic updates

### Future Enhancements
- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSocket/Socket.io)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Blockchain integration for report verification
- [ ] Integration with government databases

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Support & Community

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/Amanmeena0/Safe-sphere/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/Amanmeena0/Safe-sphere/discussions)
- **Email**: For direct support, contact the maintainers

---

## 🙏 Acknowledgments

- **Clerk** - Authentication infrastructure
- **HuggingFace** - LLM and embedding models
- **ChromaDB** - Vector database
- **FastAPI** - Backend framework
- **React** - Frontend library
- **TailwindCSS** - Styling framework

---

**Safe-Sphere**: *Because community safety starts with information, preparedness, and connection.*

🛡️ Stay Safe. Stay Informed. Stay Connected.
