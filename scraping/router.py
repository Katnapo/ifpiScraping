from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from scraping.database import get_db
from scraping.models import Song as SQLAlchemySong, DownloadLink as SQLAlchemyDownloadLink
from scraping.pydantic_models import Song, DownloadLink
from scraping.service import ScraperManager

router = APIRouter()

@router.get("/songs", response_model=List[Song])
def get_songs(db: Session = Depends(get_db)):
    songs = db.query(SQLAlchemySong).all()
    return songs

@router.get("/songs/{song_id}", response_model=Song)
def get_song(song_id: int, db: Session = Depends(get_db)):
    songs = db.query(SQLAlchemySong).filter(SQLAlchemySong.id == song_id).first()
    return songs


@router.get("/songs/{song_id}/downloads", response_model=List[DownloadLink])
def get_downloads(song_id: int, db: Session = Depends(get_db)):
    downloads = db.query(SQLAlchemyDownloadLink).filter(SQLAlchemyDownloadLink.song_id == song_id).all()
    return downloads

@router.get("/scrape/{index_amount}")
def trigger_scrape(index_amount: int, db: Session = Depends(get_db)):
    scraper_manager = ScraperManager()
    scraper_manager.scrape_indexes(db, index_amount)
    return {"message": "Scraping triggered successfully"}