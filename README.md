# a2a-redteam
A2A Redteam: A simulator for adversarial testing of multi-agent AI systems, exploring rogue agent behavior, unsafe context propagation, and deception resilience.

## Agent Prototype

This project implements a minimal agent prototype using FastAPI that:

1. Exposes a `/skills` endpoint that returns the agent's capabilities
2. Exposes a `/execute` endpoint that runs modules with specified targets
3. Logs all activities and returns execution results

### Supported Skills

- `scan_nmap`: Network scanning using nmap
- `fuzz_ffuf`: Web fuzzing (currently simulated)

### API Endpoints

- `GET /`: Returns a welcome message
- `GET /skills`: Returns the agent's ID and available skills
- `POST /execute`: Executes a module with a target
- `GET /history`: Returns execution history

### Setup and Run

1. Install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn main:app --reload
   ```

3. Access the API at http://127.0.0.1:8000/
4. API documentation available at http://127.0.0.1:8000/docs

### Example Usage

```bash
# Get agent skills
curl -X GET http://127.0.0.1:8000/skills

# Execute a module
curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"module": "scan_nmap", "target": "example.com"}'

# View execution history
curl -X GET http://127.0.0.1:8000/history
```
