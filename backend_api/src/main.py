from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.analysis import router as router_analysis
from src.api.dashboard import router as router_dashboard

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_analysis)
app.include_router(router_dashboard)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Или "*" для всех (небезопасно!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
