#!/usr/bin/python3

import psycopg2
import requests
from bs4 import BeautifulSoup


def connect():
    conn = psycopg2.connect(host='db', user="postgres", database="postgres-2", password='mmuntean1!')
    cur = conn.cursor()
    cur.execute("SELECT name, description, imdb_id FROM public.movies_movie WHERE movies_movie.description='';")
    print("The number of parts: ", cur.rowcount)
    row = cur.fetchone()
    imdb_ids = []

    while row is not None:
        row = cur.fetchone()
        print(row)
        if row is not None:
            imdb_ids.append(row[2])
    for i in imdb_ids:
        url = f'https://www.imdb.com/title/{i}/'
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        plot = html_soup.find('span', class_='sc-16ede01-2 gXUyNh')
        if plot is not None:
            plot_updated = plot.text.replace("'", "`")
            cur = conn.cursor()
            cur.execute(f"UPDATE public.movies_movie SET description='{plot_updated}' WHERE movies_movie.imdb_id='{i}';")
            updated_rows = cur.rowcount
            print(updated_rows)
            conn.commit()
    cur.close()

if __name__ == '__main__':
    connect()
