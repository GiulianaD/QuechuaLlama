# QuechuaLlama

**QuechuaLlama** is the final project for the course **Tópicos Selectos en Inteligencia Artificial**. This chat application allows users to interact with a chatbot that leverages two Large Language Models (LLMs): the **Llama 3.2 3B** and a fine-tuned version designed to facilitate **Spanish-Quechua translation**, particularly on topics related to **religious and family themes**. Additionally, the chatbot provides information about deities and festivities from **Quechua, Aymara, and Guarani** traditions.

If the user poses a question outside these specified areas, the chatbot will respond with:  
> "I am sorry. I was not trained to answer this question."

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Model Overview](#model-overview)
6. [Technologies Used](#technologies-used)
7. [License](#license)

## Features

- **Spanish-Quechua Translation**: Translate common phrases, especially in religious or familial contexts.
- **Cultural Inquiry**: Ask about traditional deities, festivities, and cultural practices among the Quechua, Aymara, and Guarani peoples.
- **Multi-model Chatbot**: Utilizes two models - Llama 3.2 3B and a fine-tuned version with enhanced Quechua-specific language support.

## Installation

### Prerequisites

Ensure that you have the following installed:
- **Python 3.8+**
- **Uvicorn** for the backend server
- **Streamlit** for the frontend interface
- **Environment Variables**: Store API tokens and sensitive data in a `.env` file for secure access.

### Clone the Repository

```bash
git clone https://github.com/GiulianaD/QuechuaLlama.git
cd QuechuaLlama
```

### Install Dependencies

Navigate to each directory and install the required dependencies:

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

```

## Usage

### Running the Backend

Navigate to the backend directory and run the application with:

```bash
uvicorn main:app --reload
```

This will start the backend API server on `http://127.0.0.1:8000`.

### Running the Frontend

Navigate to the app directory and run the frontend interface using Streamlit:

```bash
streamlit run app.py
```

The Streamlit app will typically open on `http://localhost:8501`.

## Project Structure

```
QuechuaLlama/
├── backend/                     # Backend application
│   ├── main.py                  # FastAPI application entry point
│   └── services/                # Service layer containing various functionalities
│       ├── llm.py               # Interfaces for Large Language Models
│       ├── graphdb.py           # Knowledge graph services
│       ├── chat.py              # Chatbot query handling
│       └── config.py            # Configuration and environment settings
├── app/                         # Frontend application
│   └── app.py                   # Streamlit application entry point
└── README.md

```

## Model Overview

The chatbot uses two main models:
1. **Llama 3.2 3B**: A general-purpose language model for handling general queries.
2. **Fine-tuned Llama for Quechua Translation**: This model specializes in Spanish-Quechua translation, focusing on phrases common in religious and family discussions. 

## Technologies Used

- **Python 3.8+**
- **FastAPI**: For creating the backend API
- **Streamlit**: For building the frontend application interface
- **Hugging Face Hub**: Hosting and accessing language models
- **SPARQLWrapper**: For querying a knowledge graph in the backend
- **dotenv**: For managing environment variables securely