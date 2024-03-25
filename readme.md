**Technical Interview Test for IFPI **

In this repo you will find a technical test for IFPI. The test is to build a web scraping application for 
the website https://intmusic.net/ and store the data in a database.

Stack:
- Python
- FastAPI
- MariaDB

Specific stack modules can be found in the requirements.txt file. This is just an API, I have not built a frontend for this.

The application should have the following endpoints:

localhost:8000/scraping/songs
localhost:8000/scraping/songs/{song_id}
localhost:8000/scraping/songs/{song_id}/downloads
localhost:8000/scraping/scrape/{index_amount} (Index amount is the number of pages to scrape, note that putting below 2 will not work)

http://localhost:8000/docs (Swagger UI as I went through hassle of using pydantic)

**Required Installation Instructions**

1. Clone the repository

2. Install MariaDB. As of now I am running 10.11.6. 
https://mariadb.org/download/?t=mariadb&o=true&p=mariadb&r=10.11.6&os=windows&cpu=x86_64&pkg=msi

3. Accept default installation settings. You may set a password for the root user, just remember to change 
the password in the constants.py file. HeidiSQL is a good GUI for MariaDB, if you need one quick (Mysql workbench
works too). I would reccomend you install either one and run the schema file in the 'sql' folder to create the database.
(command line instructions are below but are finnicky).

4. Install Python 3.12 (or higher to avoid any issues) from https://www.python.org/downloads/


** Command Line Instructions **

1. Open a command prompt and navigate to the directory where you cloned the repository.
2. Do the following to install the database schema if you are not using a GUI (Guides listed below too):
https://dbschema.com/documentation/mariadb/
https://mariadb.com/kb/en/running-mariadb-from-the-build-directory/

Sometimes you will need to ensure that MariaDB has been shutdown. See the dbschema.com guide for that.

Navigate to mariadb installation folder > bin > 
mariadbd.exe --console
mysql -u your_username -p password_if_set
SOURCE path_to_sql_file.sql

3. Now, navigate to the directory where you cloned the repository and run the following command to install the required modules:
pip install -r requirements.txt
4. Run the following command to start the FastAPI server:

If using a virtual environment:
# If using virtualenv
.\venv\Scripts\activate

# If using venv (standard library)
.\venv\Scripts\activate.bat

navigate to the directory where you cloned the repository and run the following command to start the FastAPI server:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

NOTE: Remember to change the connection string in the constants.py file to match your MariaDB settings.

