from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from connectors.firestore_connector import FirestoreConnector

app = FastAPI()

# Allow CORS for all origins to enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MishnaRequest(BaseModel):
    chapter: str
    mishna: str
    

# ~~~~~~~~~~~~~~~ Routs ~~~~~~~~~~~~~~~
# Health check route
@app.get("/")
async def health_check():
    return "Pirkey Avot Project Server is ready!"
    
@app.post("/getmishna/")
async def get_mishna(request_data: MishnaRequest):
    return FirestoreConnector().get_mishna(request_data.chapter, request_data.mishna)
