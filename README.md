# Code Review System
**microservice-based code review system**

The project is built around two distinct services that work together seamlessly:

- **LLM Service (AI Gateway):**  
  This service is the main part of the code review process. It accepts Python function code and provides detailed suggestions on how to improve the code. This function is LLM agnostic, meaning that it can route the request to different underlying language models depending on the `LLM_PROVIDER` environment variable you set. Here’s what that means:
  - **OpenAI's GPT-4o:**  
    When `LLM_PROVIDER` is set to use OpenAI, your code review requests are forwarded to GPT-4o—a powerful remote language model known for its advanced natural language understanding and ability to provide in-depth code analysis.
  - **DeepSeek API:**  
    Alternatively, you can choose DeepSeek, another LLM which can be called using its API that specializes in code reviews. This gives you the option to use a different model if it better meets your needs or if you prefer its feedback style.
  - **Local LLM:**  
    For those who want to run the LLM model locally, the service can use a locally hosted language model via Hugging Face Transformers. We set to use Qwen/Qwen1.5-1.8B-Chat for locall LLM. 

- **Code Analysis Service:**  
  This service has two main functions.
  - **analyze/start:**  
    This API handle the process of downloading a repository.
  - **analyze/function:**  
    Given the job id of the downloaed git repo, it extract the relevant python function and then sending the extracted code over to the LLM Service for review.

By separating the concerns—code extraction in one service and code analysis in another—the system is designed to be modular, scalable, and easier to maintain.

---

## Technology & Design

- **FastAPI & Uvicorn:** These tools provide a fast, asynchronous web server to handle API requests smoothly.
- **Docker:** Used for containerizing the services, ensuring they run consistently across different environments.
- **Poetry:** Manages project dependencies and packaging, making it easier to install and update the libraries needed.
- **LLM Integration:** Our flexible design supports multiple code review providers (remote and local), so you can choose the best tool for your workflow.
- **Testing:** We use Poetry (and optionally Nox) to run unit tests and automate various development tasks, ensuring our code remains robust as the project evolves.

---

## How to Run the Services
- **docker-compose up --build**
  This command builds the Docker images (if they haven't been built already) and then starts both the LLM Service (on port 8000) and the Code Analysis Service (on port 8001).