from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import qrcodeRoutes, urlsRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {'msg': 'Root'}

app.include_router(qrcodeRoutes.router)
app.include_router(urlsRoutes.router)