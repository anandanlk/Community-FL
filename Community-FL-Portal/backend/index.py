import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import user, infra
from dotenv import load_dotenv

# Get environment variables
load_dotenv()
origins = os.getenv("ORIGINS").split(',')
port = int(os.getenv("PORT"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(infra)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)