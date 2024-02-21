import pandas as pd
import sqlite3

# read dataframes
tracks_df = pd.read_csv(r'exercise_data/tracks.csv')
albums_df = pd.read_csv(r'exercise_data/albums.csv')
playlists_df = pd.read_csv(r'exercise_data/playlists.csv')
artists_df = pd.read_csv(r'exercise_data/artists.csv')

type(artists_df.iloc[0,0])

tracks_df = tracks_df.astype(str).replace('nan', None)
playlists_df = playlists_df.astype(str).replace('nan', None)
albums_df = albums_df.astype(str).replace('nan', None)
artists_df = artists_df.astype(str).replace('nan', None)

# arrange playlist_track table
def string_to_list(tracks):
    if isinstance(tracks, str):
        tracks = [element for element in tracks.split(',')]
    return tracks
    
playlists_df['Tracks'] = playlists_df['Tracks'].apply(string_to_list)

track_in_playlist = playlists_df.explode('Tracks')[['PlaylistId','Tracks']]
track_in_playlist.dropna(inplace = True)
track_in_playlist.rename(columns={'Tracks':'TrackId'}, inplace = True)

playlists_df = playlists_df[['PlaylistId', 'Name']]

# create tables 
connection = sqlite3.connect('musify_database.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE playlist(
               PlaylistID INT PRIMARY KEY,
               Name TEXT 
    )
""")

cursor.execute("""
    CREATE TABLE artist(
               ArtistId INT PRIMARY KEY,
               Name TEXT
    )
""")

cursor.execute("""
    CREATE TABLE album(
               AlbumId INT PRIMARY KEY,
               Title TEXT,
               ArtistId INT,
               FOREIGN KEY(ArtistId) REFERENCES artist(ArtistId))
""")

cursor.execute("""
    CREATE TABLE track(
               TrackId INT PRIMARY KEY,
               Name TEXT,
               AlbumId INT,
               Composer TEXT,
               Milliseconds INT,
               Bytes INT,
               FOREIGN KEY(AlbumId) REFERENCES album(AlbumId))
""")

cursor.execute("""
    CREATE TABLE track_in_playlist(
               PlaylistId INT ,
               TrackId INT,
               PRIMARY KEY(PlaylistId, TrackId),
               FOREIGN KEY(PlaylistId) REFERENCES playlist(PlaylistId),
               FOREIGN KEY(TrackId) REFERENCES track(TrackId))
""")

# populate tables
def populate_table(table_name, data_frame):
    data = [tuple(data_frame.iloc[row,:]) for row in range(data_frame.shape[0])]

    number_of_variables = '?'
    for i in range(data_frame.shape[1]-1):
        number_of_variables += ',?'

    query = f'INSERT INTO {table_name} VALUES({number_of_variables})'

    cursor.executemany(query, data)

populate_table('track', tracks_df)
populate_table('artist', artists_df)
populate_table('album', albums_df)
populate_table('playlist', playlists_df)
populate_table('track_in_playlist',track_in_playlist)
connection.commit()

