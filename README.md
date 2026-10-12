# Alt-nature 🌿

Alt-nature is an open-source AI agent system designed to drag software engineers away from their screens and into nature. By combining open-weight model inference with environmental grounding , speech synthesis , and durable persistence , Alt-nature delivers screen-free outdoor audio quests.

Real outdoor exploration happens where cell reception dies. By leveraging open-weight models like **Gemma**, Alt-nature guarantees zero latency, absolute privacy for real-time outdoor locations, and complete independence from closed proprietary APIs. You get full control over your prompt pipelines and system guardrails without vendor lock-in.

---

## 🛠️ Tech Stack 

- **Core AI Model:** **Gemma** (open-weight model for dynamic quest generation)
- **Voice Narration:** **ElevenLabs API** (for hands-free, screen-free audio briefings)
- **Data & Persistence:** **MongoDB Atlas** (for storing active quests, reflections, and user history)
- **Environmental Grounding:** **SerpAPI** (for real-time weather and seasonal status)
- **Agent Observability:** **Sentry Agent Tracing** (tracking execution telemetry, routing, and inference fallbacks)

---

## ⚙️ Quickstart

1. **Clone and Setup Environment:**
   ```bash
   git clone 
   cd Alt-nature
   cp .env.example .env

2. **Install Dependencies:**

```bash
pip install -r requirements.txt

```


3. **Run the FastAPI Backend:**
```bash
python -m uvicorn app.main:app --reload --port 8000

```


4. **Launch the Streamlit UI (in a separate terminal):**
```bash
streamlit run frontend/streamlit_app.py

```

