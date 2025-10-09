# AURA - Conversational Data Platform MVP

This project is the backend implementation for Phase 1 of AURA, the "Analyst in a Box."

## Core Architecture

The system is built on a microservices-based architecture featuring a Multi-Agent System (MAS) for its core logic. The key innovation is a **Generator-Critic feedback loop** to ensure the quality and security of AI-generated code before execution.

- **Orchestration Service (MAS):** The brain of the operation, managing the agent workflow.
- **Generator Agent:** Proposes a plan and writes the initial code to answer a user's query.
- **Critic Agent:** Reviews the generated code for correctness, security, and efficiency.
- **Execution Sandbox:** A secure, isolated environment for running the validated code against a database.

## Setup Instructions

1.  **Enable the Google Cloud AI Companion API:**
    * Go to the Google Cloud Console.
    * Select the project you want to use.
    * In the search bar, find and enable the **"Cloud AI Companion API"**. This is required for the Gemini extension to function.

2.  **Set Up Environment:**
    * Create a `.env` file and populate it with your API key and other credentials as shown in the `.env.example` file.

3.  **Install Dependencies:**
    * `pip install -r requirements.txt`

4.  **Run the Application:**
    * `uvicorn orchestration_service.main:app --reload`

## Project Structure

```
aura-backend/
├── orchestration_service/
│   ├── __init__.py
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── generator_agent.py
│   │   └── critic_agent.py
│
├── shared/
│   ├── __init__.py
│   └── models.py
│
├── .env
└── requirements.txt
```
