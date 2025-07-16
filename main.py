from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import shlex
import shutil
import logging
import uuid
import datetime
import json
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("agent-001")

app = FastAPI(title="Agent-001", description="A2A Red Team Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExecuteRequest(BaseModel):
    module: str
    target: str
    parameters: Optional[Dict[str, Any]] = None

class ExecuteResponse(BaseModel):
    execution_id: str
    module: str
    target: str
    output: str
    status: str
    timestamp: str
    error: Optional[str] = None

# Store execution history
execution_history: List[ExecuteResponse] = []

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello from Agent-001!"}

@app.get("/skills")
async def skills():
    logger.info("Skills endpoint accessed")
    return {
        "agent_id": "agent-001",
        "skills": ["scan_nmap", "fuzz_ffuf"],
        "description": "Red team agent with network scanning and fuzzing capabilities"
    }

@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    execution_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    logger.info(f"Execute request received - ID: {execution_id}, Module: {request.module}, Target: {request.target}")
    
    response = ExecuteResponse(
        execution_id=execution_id,
        module=request.module,
        target=request.target,
        output="",
        status="failed",
        timestamp=timestamp
    )
    
    try:
        if request.module == "scan_nmap":
            # Check if nmap is installed
            if shutil.which("nmap"):
                # Use shlex.quote to safely escape the target parameter
                safe_target = shlex.quote(request.target)
                command = f'nmap -sV {safe_target}'
                logger.info(f"Executing command: {command}")
                output = subprocess.getoutput(command)
                response.output = output
                response.status = "success"
            else:
                error_msg = "nmap not found. Please install nmap to use this feature."
                logger.error(error_msg)
                response.output = error_msg
                response.error = "Command not found"
        elif request.module == "fuzz_ffuf":
            command = f'echo "Running ffuf on {request.target}"'
            logger.info(f"Executing command: {command}")
            output = subprocess.getoutput(command)
            response.output = output
            response.status = "success"
        else:
            error_msg = f"Unsupported module: {request.module}"
            logger.error(error_msg)
            response.error = error_msg
            raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        error_msg = f"Error executing {request.module}: {str(e)}"
        logger.error(error_msg)
        response.error = error_msg
    
    # Store execution in history
    execution_history.append(response)
    
    return response

@app.get("/history")
async def get_history():
    """Return execution history"""
    logger.info("History endpoint accessed")
    return execution_history

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.datetime.now()
    response = await call_next(request)
    process_time = datetime.datetime.now() - start_time
    logger.debug(f"Request {request.method} {request.url.path} processed in {process_time.total_seconds():.4f}s")
    return response

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Agent-001 server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 