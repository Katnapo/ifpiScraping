import mariadb
from constants import Constants

def save_song_data(song_data):
    """
    Save the scraped song data to the database.

    Args:
        song_data (list): A list of dictionaries containing the scraped song data.
    """
    try:
        # Connect to the MariaDB database
        conn = mariadb.connect(
            user=Constants.DB_USER,
            password=Constants.DB_PASSWORD,
            host=Constants.DB_HOST,
            port=Constants.DB_PORT,
            database=Constants.DB_NAME
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Iterate over the song data
        for song in song_data:
            title = song['title']
            date = song['date']
            download_links = song['download_link']
            url = song['url']

            # Insert the song data into the songs table
            insert_song_query = "INSERT INTO songs (song_title, page_url, date) VALUES (%s, %s, %s)"
            insert_song_values = (title, url, date)
            cursor.execute(insert_song_query, insert_song_values)

            # Get the inserted song's ID
            song_id = cursor.lastrowid

            # Insert or update the download links into the download_links table
            for download_link in download_links:
                # Check if the download link already exists
                check_download_link_query = "SELECT id FROM download_links WHERE download_url = %s"
                check_download_link_values = (download_link,)
                cursor.execute(check_download_link_query, check_download_link_values)
                existing_download_link = cursor.fetchone()

                if existing_download_link:
                    # Update the existing download link with the new song_id
                    update_download_link_query = "UPDATE download_links SET song_id = %s WHERE id = %s"
                    update_download_link_values = (song_id, existing_download_link[0])
                    cursor.execute(update_download_link_query, update_download_link_values)
                else:
                    # Insert the download link into the download_links table
                    insert_download_link_query = "INSERT INTO download_links (song_id, download_url) VALUES (%s, %s)"
                    insert_download_link_values = (song_id, download_link)
                    cursor.execute(insert_download_link_query, insert_download_link_values)

        # Commit the changes
        conn.commit()

    except mariadb.IntegrityError as e:
        print(f"Integrity error occurred: {e}")
    except mariadb.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()

import datetime

def save_max_page(max_page):
    """
    Save the maximum page number to the database.

    Args:
        max_page (int): The maximum page number.
    """
    try:
        # Connect to the MariaDB database
        conn = mariadb.connect(
            user=Constants.DB_USER,
            password=Constants.DB_PASSWORD,
            host=Constants.DB_HOST,
            port=Constants.DB_PORT,
            database=Constants.DB_NAME
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Get the current timestamp
        current_timestamp = datetime.datetime.now()

        # Insert the maximum page number into the variables table
        insert_max_page_query = "INSERT INTO variables (variable_type_id, data, timestamp) VALUES (1, %s, %s)"
        insert_max_page_values = (str(max_page), current_timestamp)
        cursor.execute(insert_max_page_query, insert_max_page_values)

        # Commit the changes
        conn.commit()

    except mariadb.Error as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()