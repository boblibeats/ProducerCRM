from fastapi import FastAPI

app = FastAPI()

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