fastapi_app/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py
│   │   │   │   ├── users.py
│   │   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   ├── dependencies.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── user_service.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── ollama_helper.py
│   │   ├── response_handler.py
│   │   ├── __init__.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   ├── test_chat.py
│   ├── test_users.py
│   ├── __init__.py
│
├── requirements.txt
├── .env
├── run.py
└── README.md
