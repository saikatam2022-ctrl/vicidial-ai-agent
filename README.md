# 🤖 Vicidial AI Agent

A fully self-hosted, conversational AI SIP agent that integrates with [Vicidial](http://www.vicidial.org/) to handle inbound/outbound calls using real-time transcription, LLMs, and TTS.

## 🏗 Architecture

```
vicidial-ai-agent/
├── agent/            # SIP handling, STT, TTS, LLM
│   ├── sip_client.py
│   ├── audio_stream.py
│   ├── stt_whisper.py
│   ├── tts_coqui.py
│   └── llm_engine.py
├── vicidial/         # Vicidial API + call flow
│   ├── vicidial_api.py
│   └── call_flow.py
├── config/           # .env credentials & prompt templates
│   ├── credentials.env
│   └── prompts/
│       └── sales_assistant.txt
├── docker/           # Dockerfile and container configs
│   └── Dockerfile
├── run.py            # Entry point
└── README.md
```

## ⚙ Features

* 📞 SIP registration and audio streaming
* 🧠 Whisper-based transcription (via whisper.cpp or API)
* 💬 LLM-based agent replies (OpenAI, Groq, LMStudio, etc.)
* 🔊 Coqui TTS or any self-hosted/remote TTS backend
* 📈 Vicidial Agent API integration (Pause, Dispo, Transfer)

## 🚀 Setup

```bash
git clone https://github.com/saikatam2022-ctrl/vicidial-ai-agent.git
cd vicidial-ai-agent
cp config/credentials.env.example config/credentials.env
docker build -t vicidial-ai-agent .
docker run --env-file=config/credentials.env vicidial-ai-agent
```

## 🔑 Requirements

* Docker or Python 3.10+
* Vicidial server with SIP credentials
* LLM API key (OpenAI / Groq / LMStudio / Ollama / Localhost)
* STT (whisper.cpp or API) and TTS (Coqui or similar)

## 🧠 Prompt Configuration

Edit `config/prompts/sales_assistant.txt` to guide the LLM’s personality and behavior during calls.

## 🐄 Integrations

| Service   | Integration                     | Self-hosted Option? |
| --------- | ------------------------------- | ------------------- |
| SIP Audio | `pjsua` or `baresip`            | ✅ Yes               |
| STT       | Whisper API / Local whisper.cpp | ✅ Yes               |
| LLM       | OpenAI / Mistral / Local GGUF   | ✅ Yes               |
| TTS       | Coqui TTS / ElevenLabs          | ✅ Yes               |
| Vicidial  | HTTP API (`vicidial_api.py`)    | ✅ Yes               |

## 📂 Folder Breakdown

* `agent/` – handles SIP, audio, and AI brain
* `vicidial/` – handles dialer interaction
* `config/` – credentials and prompt configuration
* `docker/` – containerization setup

## 🛠 In Development

* Docker Compose for full local stack
* Interactive call simulation
* Logging and analytics per call

---

### 👨‍💻 Maintainer

Built with ❤️ by [Saikat Mitra](https://github.com/saikatam2022-ctrl)

---

**PRs Welcome!** Open an issue if you'd like to collaborate.
