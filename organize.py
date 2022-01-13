import pandas as pd

"======================//Specific Cols That I Need// =============="
col_list_vgsales = ["name", "platform", "release_date", "publisher", "na_sales", "eu_sales", "jp_sales", "other_sales",
                    "global_sales"]

df_metacritic = pd.read_csv("metacritic.csv")
df_vgsales = pd.read_csv("vgsales_full_third.csv", usecols=col_list_vgsales)

"==============//Clear Space From This Cols//======================="
df_vgsales[["name", "platform"]] = df_vgsales[["name", "platform"]].apply(lambda x: x.str.strip())

"==============//Rename vgsales Cols//=============================="
df_vgsales.rename(columns={'name': 'Name', 'platform': 'Platform'}, inplace=True)

platform_rewording_dict = {'PS3': 'PlayStation 3',
                           'X360': 'Xbox 360',
                           'PC': 'PC',
                           'WiiU': 'Wii U',
                           '3DS': '3DS',
                           'PSV': 'PlayStation Vita',
                           'iOS': 'iOS',
                           'Wii': 'Wii',
                           'DS': 'DS',
                           'PSP': 'PSP',
                           'PS2': 'PlayStation 2',
                           'PS': 'PlayStation',
                           'XB': 'Xbox',
                           'GC': 'GameCube',
                           'GBA': 'Game Boy Advance',
                           'DC': 'Dreamcast',
                           'PS4': 'PlayStation 4',
                           'XOne': 'Xbox One',
                           'NS': 'Switch'
                           }

df_vgsales[["Platform"]] = df_vgsales[["Platform"]].replace(platform_rewording_dict)

df_merge = pd.merge(left=df_metacritic, right=df_vgsales, left_on=["Name", "Platform"], right_on=["Name", "Platform"],
                    how="left")

print(df_vgsales.head())
print(df_metacritic.head())
print(df_merge.shape[0], df_merge.shape[1])

"====================//Drop NaN and Zero Values//=============="
df_merge.dropna(subset=['global_sales'], inplace=True)
df_merge = df_merge[df_merge.global_sales != '0.00m']


df_merge = df_merge[~df_merge['Genre'].isin(
    ['Massively Multiplayer Online', 'Compilation', 'Sim', 'Breeding/Constructing', 'Japanese-Style'])]

df_merge = df_merge[df_merge.Rating != 'K-A']
df_merge['release_date'] = df_merge['release_date'].replace({'N/A': None}, regex=True)
df_merge.dropna(subset=['release_date'], inplace=True)
"==================//Remove 'm' and Replace Nane with Zero from sales Cols//============="
sales_cols = ["na_sales", "eu_sales", "jp_sales", "other_sales", "global_sales"]
df_merge[sales_cols] = df_merge[sales_cols].replace({'m': ''}, regex=True)

df_merge[["User_Score"]] = df_merge[["User_Score"]].replace({'tbd': None}, regex=True)
df_merge[sales_cols] = df_merge[sales_cols].fillna(0)


def fun(num):
    num = str(num).rstrip()
    date = int(num[-2:])
    if date > 21:
        return "19" + str(date)
    else:
        if 0 <= date < 10:
            return "200" + str(date)
        else:
            return "20" + str(date)


df_merge['release_date'] = df_merge['release_date'].apply(lambda x: fun(x), convert_dtype=True)

convert_dict = {"na_sales": float,
                "eu_sales": float,
                "jp_sales": float,
                "other_sales": float,
                "global_sales": float,
                "User_Score": float,
                "release_date": float
                }
df_merge = df_merge.astype(convert_dict)
print(df_merge.info())

header_finally = {'publisher': 'Publisher',
                  'na_sales': 'NA_Sales',
                  'eu_sales': 'EU_Sales',
                  'jp_sales': 'JP_Sales',
                  'other_sales': 'Other_Sales',
                  'global_sales': 'Global_Sales',
                  'release_date': 'Year_of_Release'}

df_merge.rename(columns=header_finally, inplace=True)
df_merge = df_merge[['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales',
                     'Other_Sales',
                     'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'User_Count', 'Developer', 'Rating']]

print(df_merge['Genre'].value_counts())

df_merge.to_csv("merge.csv", index=False)
