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
- **Dual Bot Architecture**: Intelligently redirects queries to specialized bots based on the question type.
- **PostgreSQL Database**: Stores conversation history for enhanced contextual understanding.

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
docker compose build
```

**Run the Docker container**
```
docker compose up
```

### Technologies Used:
- **Flask**: A lightweight web framework used for running the chatbot server.
- **Docker**: Ensures easy deployment and scalability of the application in isolated environments.
- **LLM** (Large Language Model): Used for natural language understanding and generation, allowing the chatbot to converse intelligently.
- **RAG** (Retrieval-Augmented Generation): Augments the LLM with real-time data retrieval for more accurate and relevant answers.
- **Memory**: Keeps track of ongoing conversations to provide a personalized experience across multiple interactions.
- **PostgreSQL**: Robust relational database for storing conversation history and user data.
- **Dual Bot Architecture**: Routes queries to specialized bots for more accurate responses to different types of agricultural questions.

### Contributors:
- [Contributor Name 1] - [Role/Contribution]
- Tuan Nguyen Ngo Anh - Frontend Features, Backend Development, Deploying Pipeline
- [Contributor Name 3] - [Role/Contribution]
- [Contributor Name 4] - [Role/Contribution]

Built for Hack Illinois 2025, powered by ACM@UIUC

For more information about Hack Illinois, visit https://hackillinois.org/.