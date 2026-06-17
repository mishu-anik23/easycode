from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, plan, diff, apply, index, search, auth
from .core.logging import configure_logging

app = FastAPI(title="EasyCode API", version="0.1.0")

configure_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(plan.router, prefix="/plan", tags=["plan"])
app.include_router(diff.router, prefix="/diff", tags=["diff"])
app.include_router(apply.router, prefix="/apply", tags=["apply"])
app.include_router(index.router, prefix="/index", tags=["index"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"status": "EasyCode backend is running"}
