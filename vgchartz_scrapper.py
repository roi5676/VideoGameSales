from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pages = 50
genres = ['Action', 'Action-Adventure', 'Adventure', 'Board+Game', 'Education', 'Fighting', 'Misc', 'MMO', 'Music',
          'Party', 'Platform', 'Puzzle', 'Racing', 'Role-Playing', 'Sandbox', 'Shooter', 'Simulation', 'Sports',
          'Strategy', 'Visual+Novel']
rank = []
gname = []
platform = []
release_date = []
publisher = []
sales_na = []
sales_eu = []
sales_jp = []
sales_ot = []
sales_gl = []
developer = []
total_shipped = []
game_url = []
game_genre = []
game_url_string = []
count = 0
fails = 0

urlhead = 'http://www.vgchartz.com/games/games.php?page='
urlmid = '&results=200&name=&console=&keyword=&publisher=&genre='
urltail = '&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=No'

for genre in genres:
    for page in range(1, pages):
        print(page)
        surl = urlhead + str(page) + urlmid + genre + urltail
        r = requests.get(surl)
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')
        for row in soup.find_all('tr'):
            try:
                col = row.find_all('td')
                col_0 = col[0].text
                col_4 = col[4].text
                col_5 = col[5].text
                col_9 = col[6].text
                col_10 = col[10].text
                col_11 = col[11].text
                col_12 = col[12].text
                col_13 = col[13].text
                col_14 = col[14].text
                col_15 = col[15].text
                img = col[3].find('img')
                col_3 = img['alt']
                a_tag = col[2].find('a')
                url_col = a_tag['href']
                col_2 = (a_tag.text)
                url_string = url_col.rsplit('/', 2)[1]

                if len(col_0) < 6:
                    rank.append(col_0)
                    gname.append(col_2)
                    publisher.append(col_4)
                    developer.append(col_5)
                    total_shipped.append(col_9)
                    sales_gl.append(col_10)
                    sales_na.append(col_11)
                    sales_eu.append(col_12)
                    sales_jp.append(col_13)
                    sales_ot.append(col_14)
                    release_date.append(col_15)
                    platform.append(col_3)
                    game_url.append(url_col)
                    game_genre.append(genre)
                    game_url_string.append(url_string)
                    count += 1
            except:
                fails += 1
                continue
print('vg_chartz count = ' + str(count))
print('vg_chartz fails = ' + str(fails))

columns = {'total_shipped': total_shipped,
           'developer': developer,
           'rank': rank,
           'name': gname,
           'platform': platform,
           'release_date': release_date,
           'publisher': publisher,
           'na_sales': sales_na,
           'eu_sales': sales_eu,
           'jp_sales': sales_jp,
           'other_sales': sales_ot,
           'global_sales': sales_gl,
           'game_genre': game_genre,
           'game_url': game_url,
           'game_url_string': game_url_string}

df = pd.DataFrame(columns)
df = df[['total_shipped', 'developer', 'rank', 'name', 'platform', 'release_date', 'publisher', 'na_sales', 'eu_sales',
         'jp_sales', 'other_sales', 'global_sales', 'game_genre', 'game_url', 'game_url_string']]
df.to_csv("vgsales_full_third.csv", sep=",", encoding='utf-8')

