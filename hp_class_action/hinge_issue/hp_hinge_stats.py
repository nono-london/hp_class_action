import pandas as pd

result_df = pd.read_csv('hp_hinges_issues.csv',
                        sep=',',
                        parse_dates=['post_datetime'])
print(result_df.drop_duplicates(subset=['post_id', 'post_datetime'],keep='first'))
