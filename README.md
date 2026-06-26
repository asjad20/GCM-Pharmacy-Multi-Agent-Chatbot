# Multi-Agent Pharmacy Assistant

A production multi-agent AI system built for a healthcare pharmacy. Four specialized agents handle patient intake, qualification, and routing — with mid-conversation switching driven by LangGraph's state machine architecture.

Built with **LangGraph**, **Django REST Framework**, and **Google Gemini 2.5 Flash**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-yellow)

---

## What It Does

A patient opens the chat and talks to **Sophia**, the front-facing general assistant. Based on what they ask, Sophia dynamically routes the conversation to one of three specialist agents — each with its own knowledge, intake flow, and database model. Agents can route *back* to Sophia or to each other, mid-conversation, without losing context.

**Example flow:**
```
Patient: "Hi, I need help"
→ Sophia responds (general assistant)

Patient: "I'm interested in weight loss medication"
→ Sophia calls weight_loss_tool → Weight Loss agent takes over

Patient: "Actually, do you also have glucose monitors?"
→ Weight Loss agent calls cgm_agent_tool → CGM agent takes over

Patient: "What services do you offer overall?"
→ CGM agent calls sophia_tool → Sophia takes back over
```

All routing happens through LangGraph tool-calling — the LLM decides which agent to invoke based on the query, and the graph state carries `session_id` across every transition.

---

## Architecture

```
                         ┌─────────────────┐
                         │   Frontend UI   │
                         │  (Landing Page  │
                         │   + Chat UI)    │
                         └────────┬────────┘
                                  │ REST API
                         ┌────────▼────────┐
                         │   Django DRF    │
                         │   views.py      │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │    main()       │
                         │  Agent Router   │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼──────┐ ┌─────────▼──────┐ ┌─────────▼──────┐
    │  Weight Loss   │ │    CGM Agent   │ │   DME Agent    │
    │    Agent       │ │                │ │                │
    └─────────┬──────┘ └─────────┬──────┘ └─────────┬──────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                         ┌────────▼────────┐
                         │  Sophia Agent   │
                         │ (Front-facing)  │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              ┌─────▼───┐  ┌─────▼───┐  ┌─────▼────┐
              │ Patient  │  │ Convo   │  │Cloudinary│
              │   DBs    │  │ History │  │ Uploads  │
              └─────────┘  └─────────┘  └──────────┘
```

### Agent Details

| Agent | Role | Tools | Data Collected |
|-------|------|-------|----------------|
| **Sophia** | Front-facing general assistant. Handles identity, services overview, medication questions, insurance, refills, and routes to specialists. | `weight_loss_tool`, `cgm_agent_tool`, `dme_agent_tool`, `sophia_db_info` | Name, DOB, phone, medication, inquiry type, callback requests |
| **Weight Loss** | GLP-1 medication specialist. Handles semaglutide/tirzepatide intake, telehealth routing, prescription collection, and delivery setup. | `sophia_tool`, `cgm_agent_tool`, `dme_agent_tool`, `weightloss_db_info` | Name, phone, prescription status, delivery method, callback |
| **CGM** | Continuous Glucose Monitor specialist. Runs full clinical qualification flow — diabetes diagnosis, insulin status, A1c, doctor info, insurance verification. | `sophia_tool`, `weight_loss_tool`, `dme_agent_tool`, `cgm_db_info` | Full clinical profile, insurance details, doctor info, prescription/telehealth status |
| **DME** | Durable Medical Equipment specialist. Handles CPAP, wheelchairs, braces, oxygen — with Texas-compliant prescription requirement logic based on item category and payment method. | `sophia_tool`, `weight_loss_tool`, `cgm_agent_tool`, `dme_db_info` | Name, phone, item requested, insurance, prescription status, compliance |

### How Routing Works

Each agent is a **LangGraph StateGraph** with a chatbot node and a tool node. The LLM is bound to a list of tools that includes the other agents as callable functions. When the LLM decides a query belongs to a different agent, it calls that agent's tool — which compiles and invokes a new graph with the same `session_id`.

```python
# Each agent is both a graph node AND a tool callable by other agents
sophie_agent_tool_list = [weight_loss_tool, cgm_agent_tool, dme_agent_tool, sophia_db_info]
weight_loss_agent_tools_list = [sophia_tool, cgm_agent_tool, dme_agent_tool, weightloss_db_info]
```

Agent selection state is persisted in the database via `modelselection`, so the `main()` router knows which agent to invoke on the next message without re-routing through Sophia every time.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Google Gemini 2.5 Flash |
| **Agent Framework** | LangGraph (StateGraph, ToolNode, tools_condition) |
| **Backend** | Django REST Framework |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Image Storage** | Cloudinary |
| **Frontend** | Single-file HTML/CSS/JS with glassmorphism UI |
| **Key Libraries** | `langchain-google-genai`, `langchain-core`, `langgraph`, `cloudinary`, `python-dotenv` |

---

## Project Structure

```
weightloss_project/
├── weightloss_agent/
│   ├── agent.py          # All 4 agents, tool definitions, routing logic, main()
│   ├── models.py          # Django models for each patient type + conversation history
│   ├── views.py           # DRF API views (chat, upload, session)
│   ├── urls.py            # API routing
│   └── admin.py           # Admin registration
├── weightloss_project/
│   ├── settings.py
│   └── urls.py
├── frontend.html          # Landing page + chat UI (single file)
├── manage.py
├── .env                   # API keys (not committed)
└── .gitignore
```

---

## Setup

### Prerequisites
- Python 3.11+
- Google Gemini API key
- Cloudinary account (for image uploads)

### Installation

```bash
# Clone
git clone https://github.com/asjad20/GCM-Pharmacy-Multi-Agent-Chatbot.git
cd GCM-Pharmacy-Multi-Agent-Chatbot

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Fill in: GEMINI_API, CLOUDINARY_NAME, CLOUDINARY_API, CLOUDINARY_API_SECRET

# Database
python manage.py migrate

# Run
python manage.py runserver
```

Open `frontend.html` in your browser. The API runs on `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/weightloss_agent/chat-session/` | Create a new session |
| `GET` | `/weightloss_agent/Pharmacy-Agent/?session_id=` | Get current agent info and upload limits |
| `POST` | `/weightloss_agent/Pharmacy-Agent/` | Send a message (query + session_id) |
| `POST` | `/weightloss_agent/upload/` | Upload a document (file + session_id + photo_slot) |

---

## Key Engineering Decisions

**Why LangGraph over a simple router?** A regex or keyword router can't handle "Actually, do you also have glucose monitors?" mid-conversation about weight loss. The LLM needs to *understand* the intent shift and *decide* to invoke the CGM agent. LangGraph's tool-calling pattern lets each agent be both a graph node and a callable tool, so routing is a natural LLM decision, not a brittle rule.

**Why session_id via shared state instead of tool parameters?** Google Gemini's function-calling schema rejects `Optional` types and struggles with parameters the LLM shouldn't control. `session_id` is injected via a shared dict (`_ctx`) so it never appears in any tool signature — the LLM can't hallucinate a wrong session ID.

**Why separate DB models per agent?** Each agent collects fundamentally different data (clinical history for CGM vs. item category for DME vs. delivery preference for weight loss). A single polymorphic model would be messier than four clean, purpose-built tables.

---

## Environment Variables

```
GEMINI_API=your_gemini_api_key
CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## License

Private project — built for a healthcare client. Code shared for portfolio/demonstration purposes.
