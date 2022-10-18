import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from hp_class_action.hp_database.mdb_handlers import (fetch_query)

pd.set_option('display.max_columns', None)


# pd.set_option('display.max_rows', None)
# LOCAL_FILE_NAME: str = str(Path().joinpath(get_project_download_path(), 'hp_hinges_issues.csv'))


def get_mdb_dataset(from_year: int = 2018) -> list:
    """Get relevant data from mdb"""
    sql_query: str = """
            SELECT a.hp_post_id, a.post_datetime, b.username, a.me_too, a.post_url
            FROM forum_posts a INNER JOIN hp_users b
                    ON a.user_id=b.user_id
            WHERE a.post_datetime >= MAKEDATE(%s, 1)
            ORDER BY a.post_datetime DESC
            
        """
    results: list = fetch_query(sql_query=sql_query,
                                variables=(from_year,))
    for row_dict in results:
        if row_dict['me_too'] is not None:
            row_dict['me_too'] = json.loads(row_dict['me_too'])

    return results


def clean_metoo_user_details(me_to_user_details: list) -> pd.DataFrame:
    """Select the oldest time a user has claimed on another chat that he had the same issue"""
    user_details: list = []
    for row_dicts in me_to_user_details:
        for row_dict in row_dicts:
            user_details.append(row_dict)

    user_detail_df: pd.DataFrame = pd.DataFrame(user_details)
    user_detail_df.sort_values(by=['username', 'post_datetime'],
                               ascending=[True, False],
                               inplace=True)
    user_detail_df.drop_duplicates(subset=['username'],
                                   keep='first',
                                   inplace=True,
                                   ignore_index=True)
    user_detail_df['post_datetime'] = pd.to_datetime(user_detail_df['post_datetime'])
    return user_detail_df


def all_claims(from_year: int = 2018):
    """Returns a df containing claims on forum and claims in private message (me_too)"""
    mdb_results = get_mdb_dataset(from_year=from_year)
    mdb_df: pd.DataFrame = pd.DataFrame(mdb_results)

    metoo_user_details: [dict] = [x['me_too'] for x in mdb_results if x['me_too'] is not None]

    meeto_df = clean_metoo_user_details(me_to_user_details=metoo_user_details)

    # add claimed
    mdb_df['claimed'] = True
    meeto_df['claimed'] = False

    union_df = pd.concat([mdb_df[['post_datetime', 'username', 'claimed']],
                          meeto_df[['post_datetime', 'username', 'claimed']]],
                         join='outer',
                         ignore_index=True)
    clean_df = union_df.drop_duplicates(subset=['username'],
                                        keep='first',
                                        inplace=False,
                                        ignore_index=True,

                                        )
    clean_df = clean_df.sort_values(by=['post_datetime', 'username'],
                                    ascending=[True, True],
                                    inplace=False,
                                    ignore_index=True)

    print(f'len mdb_df:     {len(mdb_df):,}')
    print(f'len metoo_df:   {len(meeto_df):,}')
    print(f'len union_df:   {len(union_df):,}')
    print(f'len clean_df:   {len(clean_df):,}')
    print(f'clean_df:\n{clean_df}')

    return clean_df


def chart_claim_hidden_claims(from_year: int = 2018):
    result_df: pd.DataFrame = all_claims(from_year=from_year)

    # count record by True/False
    year_claim_df = result_df.groupby([
        result_df['post_datetime'].dt.year,
        result_df['claimed']]
    ).count()
    # calculate percent
    year_claim_df['percent'] = year_claim_df['username'].groupby(level=0).transform(lambda x: (x / x.sum()).round(5))
    # get rid of uncenessary columns
    year_claim_df = year_claim_df[['percent']]
    year_claim_df.reset_index(drop=False, inplace=True)

    year_claim_df['claimed_pct'] = year_claim_df.loc[year_claim_df['claimed'] == True, 'percent']
    year_claim_df['unclaimed_pct'] = year_claim_df.loc[year_claim_df['claimed'] == False, 'percent']
    year_claim_df.fillna(0, inplace=True)
    print(year_claim_df)

    ax = year_claim_df.pivot('post_datetime',
                             'claimed',
                             'percent').rename(columns={True: 'public forum',
                                                        False: 'private message'}
                                               ).plot.bar(stacked=True, color=['orange', 'turquoise'])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    plt.show()


if __name__ == '__main__':
    all_claims(from_year=2017)
