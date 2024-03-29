#!/usr/bin/python3

import psycopg2
import requests
from bs4 import BeautifulSoup


def connect():
    conn = psycopg2.connect(host='db', user="postgres", database="postgres-2", password='mmuntean1!')
    cur = conn.cursor()
    cur.execute("SELECT description, imdb_id FROM public.movies_movie WHERE movies_movie.description='';")
    update_query = "UPDATE public.movies_movie SET description=%s, poster=%s WHERE movies_movie.imdb_id=%s;"
    print("The number of parts: ", cur.rowcount)
    update_data = []
    for row in cur.fetchall():
        url = f'https://www.imdb.com/title/{row[1]}/'
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        plot = html_soup.find('span', class_='sc-16ede01-2 gXUyNh')
        poster = html_soup.find('div', class_='ipc-media ipc-media--poster-27x40 '
                                              'ipc-image-media-ratio--poster-27x40 '
                                              'ipc-media--baseAlt ipc-media--poster-l '
                                              'ipc-poster__poster-image ipc-media__img')
        print(poster.find('img')['src'])

        if plot is not None:
            data = (plot.text, poster.find('img')['src'], row[1])
            update_data.append(data)

    cur.executemany(update_query, update_data)
    conn.commit()
    cur.close()


if __name__ == '__main__':
    connect()
