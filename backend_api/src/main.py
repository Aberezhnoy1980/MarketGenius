from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth

app = FastAPI()

app.include_router(router_auth)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
