import sys
import pandas as pd
from MetaCriticScraper import MetaCriticScraper
import time
import pandas


url_metacritic = 'https://www.metacritic.com/game/'

header_finally = ['Name', 'Platform', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales',
                  'Other_Sales',
                  'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'Developer', 'Rating']

header_metacritic = ['Name', 'Platform', 'Critic_Score', 'Critic_Count', 'User_Score', 'User_Count',
                     'Developer',
                     'Rating', 'Genre']

platform_rewording_dict = {'PS3': 'playstation-3',
                           'X360': 'xbox-360',
                           'PC': 'pc',
                           'WiiU': 'wii-u',
                           '3DS': '3ds',
                           'PSV': 'playstation-vita',
                           'iOS': 'ios',
                           'Wii': 'wii',
                           'DS': 'ds',
                           'PSP': 'psp',
                           'PS2': 'playstation-2',
                           'PS': 'playstation',
                           'XB': 'xbox',
                           'GC': 'gamecube',
                           'GBA': 'game-boy-advance',
                           'DC': 'dreamcast',
                           'PS4': 'playstation-4',
                           'XOne': 'xbox-one',
                           'NS': 'switch',
                           'PS5': 'playstation-5',
                           'N64': 'n64'
                           }
col_list = ["name", "platform", "global_sales"]
df_vgsales = pd.read_csv("vgsales_full_third.csv", usecols=col_list)
df_vgsales = df_vgsales[df_vgsales.platform.isin(platform_rewording_dict.keys())]
df_vgsales.dropna(subset=['global_sales'], inplace=True)

nameList = df_vgsales.name.to_list()
platformList = df_vgsales.platform.to_list()
nameList = list(map(str.strip, nameList))
platformList = list(map(str.strip, platformList))
globalList = df_vgsales.global_sales.to_list()
count = 0

metacritic_title = []
metacritic_platform = []
metacritic_critic_score = []
metacritic_critic_count = []
metacritic_user_score = []
metacritic_user_count = []
metacritic_developer = []
metacritic_rating = []
metacritic_genre = []
print(len(nameList))
for i in range(len(nameList)):
    url = url_metacritic + platform_rewording_dict[platformList[i]] + "/" + nameList[i].replace(":", "").replace("& ",
                                                                                                                 "").replace(
        "'", "").replace(" ", "-").lower()
    scraper = MetaCriticScraper(url)
    if scraper.game['title'] == '' or scraper.game['title'] == '***':
        print("An exception occurred")
        continue
    metacritic_title.append(scraper.game['title'])
    metacritic_platform.append(scraper.game['platform'])
    metacritic_critic_score.append(scraper.game['critic_score'])
    metacritic_critic_count.append(scraper.game['critic_count'])
    metacritic_user_score.append(scraper.game['user_score'])
    metacritic_user_count.append(scraper.game['user_count'])
    metacritic_developer.append(scraper.game['developer'])
    metacritic_rating.append(scraper.game['rating'])
    metacritic_genre.append(scraper.game['genre'])
    print(str(count) + " " + metacritic_title[-1] + " , " + metacritic_platform[-1])
    count += 1

meta_columns = {'Name': metacritic_title,
                'Platform': metacritic_platform,
                'Critic_Score': metacritic_critic_score,
                'Critic_Count': metacritic_critic_count,
                'User_Score': metacritic_user_score,
                'User_Count': metacritic_user_count,
                'Developer': metacritic_developer,
                'Rating': metacritic_rating,
                'Genre': metacritic_genre,
                }


df_metacritic = pd.DataFrame(meta_columns)
df_metacritic.to_csv('metacritic.csv', header=header_metacritic, index=False)


