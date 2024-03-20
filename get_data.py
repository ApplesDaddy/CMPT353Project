import pandas as pd
import numpy as np

data = pd.read_json("challenge_set.json")

playlist_df = data["playlists"].apply(pd.Series)

#credit: https://stackoverflow.com/questions/34162625/remove-rows-with-empty-lists-from-pandas-data-frame
# remove empty lists
playlist_df = playlist_df[playlist_df['tracks'].apply(lambda x: len(x) > 0)]

# get list of tracks
track_list = []
for list in playlist_df['tracks']:
    for dic in list:
        for track in dic:
            track_list.append(dic[track])

#credit: https://stackoverflow.com/questions/1403674/make-a-new-list-containing-every-nth-item-in-the-original-list
# parse data from array and split into multiple arrays
pos = track_list[::8]
artist_name = track_list[1::8]
track_uri = track_list[2::8]
artist_uri = track_list[3::8]
track_name = track_list[4::8]
album_uri = track_list[5::8]
duration_ms = track_list[6::8]
album_name = track_list[7::8]

# turn arrays into dataframe containing track data
tracks_df = pd.DataFrame(np.array([pos, artist_name, track_uri, artist_uri, track_name, album_uri, duration_ms, album_name]).transpose(), columns = ['pos', 'artist_name', 'track_uri', 'artist_uri', 'track_name', 'album_uri', 'duration_ms', 'album_name'])

# extract playlist names from dataframe
playlist_names = []
for name in playlist_df['name']:
    playlist_names.append(name)

# create new column to store playlist that the track is in
tracks_df['playlist'] = None

#  add playlist names to dataframe containing tracks
i = 0
for ind in tracks_df.index:
    if tracks_df['pos'][ind] == '0' and ind != 0:
        i += 1
    tracks_df['playlist'][ind] = playlist_names[i]

# remove unnecessary data from dataframe
tracks_df = tracks_df.drop(labels=['pos'], axis=1)

# export dataframe to csv
tracks_df.to_csv("tracks_playlists.csv", index=False)
    