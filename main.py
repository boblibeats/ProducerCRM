from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ArtistCreate(BaseModel):
    name: str
    genre: str | None = None

fake_artists = [
    {"id": 1, "name": "Sawyer Utah", "genre": "Indie Pop"},
    {"id": 2, "name": "Lyncs", "genre": "Indie Pop"}
]

@app.get("/")
def read_root():
    return {"message": "hello producer!"}

@app.get("/artists")
def list_artists():
    return (fake_artists)

@app.get("/artists/{artist_id}")
def get_artists(artist_id:int):
    for artist in fake_artists:
        if artist["id"] == artist_id:
            return artist
    return {"error": "artist not found"}

@app.post("/artists")
def create_artist(artist: ArtistCreate):
    new_artist = {
        "id" : len(fake_artists) + 1,
        "name" : artist.name,
        "genre" : artist.genre,
    }
    fake_artists.append(new_artist)
    return new_artist