"""
A script that searches unambiguous work given artist and song title from MusicBrainzngs library.
Checks to make sure if the result is exact match of queried items.
Jinny Park
Last Edited by 082620
"""


from __future__ import unicode_literals
from __future__ import print_function
import musicbrainzngs
import sys

musicbrainzngs.set_useragent(
    "python-musicbrainzngs",
    "0.1"
    "https://github.com/jinnypark/mbquery/"
)

def show_work_details(work_list, artist_name,work_title):
    disambiguation_artist_name = ""
    artists = []
    the_title = work_list['title']
    MBID = work_list['id']

    if 'artist-relation-list' in work_list:
        for each in work_list['artist-relation-list']:
            if each['artist']:
                artist_dict = each['artist']
                artists.append(artist_dict['name'])
                disambiguation_artist_name = artist_dict.get('disambiguation', None)
                if disambiguation_artist_name is not None:
                    artists.append(disambiguation_artist_name)
                else:
                    artists.append(artist_dict['name'])

        # print("{}, by".format(work_list['title'], work_list['artist-relation-list']))
    print("MusicBrainz ID: {}".format(MBID))
    print("Title of the song: {}".format(the_title))
    print("Artists involved: {}".format(artists))
    if artist_name in artists:
        print("artist name match")
        if work_title == the_title:
            print("title match")
            print("Searched artist, '{}', exists in our artist list: {}".format(artist_name, artists))
            print("Input title '{}' matches found title: '{}'".format(work_title,the_title))
        else:
            print("This query needs to be rechecked.")
            print("Input title '{}' does NOT match found title: '{}'".format(work_title,the_title))
    else:
        print("This query needs to be rechecked. These are artists involved: {}".format(artists))
    # print("input artist name: ", artist_name, "disambiguation: ", disambiguation_artist_name)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit("usage: {} TITLE ARTIST".format(sys.argv[0]))
    # args must be inputted as strings, e.g., python search_work.py "Daft Punk" "Get Lucky"
    title, artist = args
    theTitle = title
    # output artist from the query and match it against my input artist name to compare if the artist name to raise error if there is no match
    result = musicbrainzngs.search_works(work=title, artist=artist, limit=3)

    # On sucess, result is a dictionary with a single key:
    # "release-list", which is a list of dictionaries.
    if not result['work-list']:
        sys.exit("no work found")
    for (idx, work) in enumerate(result['work-list']):
        print("match #{}:".format(idx+1))
        show_work_details(work,artist,theTitle)
        print()
