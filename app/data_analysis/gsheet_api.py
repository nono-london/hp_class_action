import json
from datetime import datetime
from time import time

import pandas as pd
import requests

GSHEET_URL: str = "https://script.google.com/macros/s/AKfycbx42OuLPncwWnsiTwX447DVCveMA_a-8GQuaxeB_h2TymNgcPL5G4-BpXG_4XapaBMruQ/exec"


def get_hp_claims_from_api() -> dict:
    """Get hp claims from Google Sheet REST API and
        Return {"download_datetime":datetime, "data": pd.DataFrame} """
    start_time = time()
    download_datetime = datetime.utcnow()
    print("retrieving data from google api")
    web_request = requests.get(url=GSHEET_URL)
    print(f"Data retrieved in: {round(time() - start_time, 1)} seconds")

    start_clean_time = time()
    print('Cleaning data')
    result_df: pd.DataFrame = pd.DataFrame(web_request.json()['data'], )
    result_df['post_datetime'] = pd.to_datetime(result_df['post_datetime'])

    # print(result_df)
    me_too_col = []
    post_tags_col = []

    # de-stringify met_too and post_tags
    for index, row in result_df.iterrows():
        if row['me_too'] is not None and row['me_too'] != "":
            # print(f"me_too is: {row['me_too']} and of type: {type(row['me_too'])}")
            me_too_json = json.loads(row['me_too'].strip('"'))
        else:
            me_too_json = None

        if row['post_tags'] is not None and row['post_tags'] != "":
            # print(f"post_tags is: {row['post_tags']} and of type: {type(row['post_tags'])}")
            post_tags_json = json.loads(row['post_tags'].strip('"'))
        else:
            post_tags_json = None

        me_too_col.append(me_too_json)
        post_tags_col.append(post_tags_json)

    print(f'Data cleaned in {round(time() - start_clean_time, 1)} seconds')
    print(f'Program ran for {round(time() - start_time, 1)}')
    return {"download_datetime": download_datetime, "data": result_df, "size": len(result_df)}


if __name__ == '__main__':
    get_hp_claims_from_api()
