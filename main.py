from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from connectors.firestore_connector import get_mishna

app = FastAPI()

# Allow CORS for all origins to enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: str
    model: str
    isBlack: bool

get_mishna("ב","א")

# ~~~~~~~~~~~~~~~ Routs ~~~~~~~~~~~~~~~
# Health check route
@app.get("/")
async def health_check():
    return "Pirkey Avot Project Server is ready!"
    
@app.post("/getmishna/")
async def get_mishna(chapter: str, mishna: str, tags: str):
    return get_mishna(chapter,mishna, tags)
