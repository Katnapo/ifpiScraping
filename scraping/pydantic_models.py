from pydantic import BaseModel
class SongBase(BaseModel):
    song_title: str
    page_url: str
    date: str | None = None  # Make 'date' optional

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True

class DownloadLink(BaseModel):
    id: int
    download_url: str
    song_id: int

    class Config:
        orm_mode = True