import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scraping.constants import Constants
from sqlalchemy.orm import Session
from scraping.models import Song, DownloadLink, Variable, VariableType

engine = create_engine(Constants.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def save_song_data(db: Session, song_title, page_url, date, download_links):
    # Check if the song already exists
    existing_song = db.query(Song).filter(Song.song_title == song_title).first()

    if existing_song:
        # Update the existing song's download links
        existing_download_links = {dl.download_url for dl in existing_song.download_links}
        new_download_links = set(download_links) - existing_download_links

        for dl in new_download_links:
            # Check if the download link already exists
            existing_download_link = db.query(DownloadLink).filter(DownloadLink.download_url == dl).first()
            if not existing_download_link:
                db_download_link = DownloadLink(download_url=dl, song=existing_song)
                db.add(db_download_link)
    else:
        try:
            # Create a new song
            new_song = Song(song_title=song_title, page_url=page_url, date=date)
            db.add(new_song)
            db.flush()  # Flush to get the new song's ID

            # Add the download links
            for dl in download_links:
                # Check if the download link already exists
                existing_download_link = db.query(DownloadLink).filter(DownloadLink.download_url == dl).first()
                if not existing_download_link:
                    db_download_link = DownloadLink(download_url=dl, song=new_song)
                    db.add(db_download_link)
        except MySQLdb.IntegrityError:
            db.rollback()

    db.commit()

def save_max_page(db: Session, max_page):
    # Check if the variable already exists
    existing_variable = db.query(Variable).join(VariableType).filter(VariableType.type == 'max_page').first()

    if existing_variable:
        # Update the existing variable
        existing_variable.data = str(max_page)
    else:
        try:
            # Create a new variable
            variable_type = db.query(VariableType).filter(VariableType.type == 'max_page').first()
            if not variable_type:
                variable_type = VariableType(type='max_page')
                db.add(variable_type)
                db.flush()

            new_variable = Variable(data=str(max_page), variable_type=variable_type)
            db.add(new_variable)

        except MySQLdb.IntegrityError:
            db.rollback()

    db.commit()
