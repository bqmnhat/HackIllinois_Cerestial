# Cerestial: ChatBot for Agriculture Planning
## Hack Illinois 2025 - ACM@UIUC

### Overview
Welcome to **Cerestial**, a cutting-edge chatbot designed for **Agriculture Planning**. Leveraging the power of **Large Language Models (LLM)**, **Retrieval-Augmented Generation (RAG)**, and **memory**, Cerestial helps farmers and agricultural planners make data-driven decisions for optimized crop management, yield predictions, and resource allocation.

Cerestial is built for **Hack Illinois 2025**, showcasing the potential of AI to transform the agriculture industry.

---

### Features:
- **Conversational AI**: Engage in intelligent discussions about agriculture planning.
- **Real-Time Data Retrieval**: Get relevant information on crop management, weather patterns, and more.
- **Memory Integration**: The chatbot remembers previous interactions for a more personalized experience.

---

### Local Development Setup

**Get Docker CLI**
```
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
curl -fsSL https://get.docker.com -o get-docker.sh
sudo chmod +x get-docker.sh
sudo sh ./get-docker.sh --dry-run
```

**Build image**
```
docker build -t cerestial ./app
```

**Run the Docker container**
```
docker run --env-file .env -p 8127:8127 cerestial
```

### Technologies Used:
- **Flask**: A lightweight web framework used for running the chatbot server.
- **Docker**: Ensures easy deployment and scalability of the application in isolated environments.
- **LLM** (Large Language Model): Used for natural language understanding and generation, allowing the chatbot to converse intelligently.
- **RAG** (Retrieval-Augmented Generation): Augments the LLM with real-time data retrieval for more accurate and relevant answers.
- **Memory**: Keeps track of ongoing conversations to provide a personalized experience across multiple interactions.

Built for Hack Illinois 2025, powered by ACM@UIUC

For more information about Hack Illinois, visit https://hackillinois.org/.
