from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Artist

app = FastAPI()

#Pydantic blueprints
class ArtistCreate(BaseModel):
    name: str
    email: str | None = None
    genre: str | None = None

class ArtistRead(BaseModel):
    id: int
    name: str
    email: str | None
    genre: str | None

    model_config = {"from_attributes":True}

#Endpoints
@app.get("/")
def read_root():
    return {"message": "hello producer!"}

@app.get("/artists", response_model=list[ArtistRead])
def list_artists(db: Session = Depends(get_db)):
    return db.query(Artist).all()

@app.get("/artists/{artist_id}", response_model=ArtistRead)
def get_artists(artist_id:int, db: Session = Depends(get_db)):
    artist = db.get(Artist, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@app.post("/artists", response_model=ArtistRead, status_code=201)
def create_artist(payload: ArtistCreate, db: Session = Depends(get_db)):
    artist = Artist(name = payload.name, email = payload.email, genre = payload.genre)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist

@app.put("/artists/{artist_id}", response_model=ArtistRead)
def update_artist(artist_id: int, payload: ArtistCreate, db: Session = Depends(get_db)):
    artist = db.get(Artist,artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    artist.name = payload.name
    artist.email = payload.email
    artist.genre = payload.genre
    db.commit()
    db.refresh(artist)
    return artist

@app.delete("/artists/{artist_id}")
def delete_artist(artist_id: int, db:Session = Depends(get_db)):
    artist = db.get(Artist,artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    db.delete(artist)
    db.commit()
    return {"detail": f"Artist {artist_id} deleted"}