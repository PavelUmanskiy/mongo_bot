from warnings import filterwarnings

import pandas as pd


filterwarnings('ignore')

SalarySum = int
DateLabel = str
ProcessedSalaryData = dict[str, list[SalarySum | DateLabel]]


def create_salary_df(
    raw_salary_data: list[dict[str, str | int]]
) -> pd.DataFrame:
    salary_df = pd.DataFrame(raw_salary_data)
    salary_df['dt'] = pd.to_datetime(salary_df['dt'])
    return salary_df


def aggregate_salary_data(
    salary_df: pd.DataFrame,
    dt_from: str,
    dt_upto: str,
    group_type: str
) -> ProcessedSalaryData:

    frequency = group_type[0].capitalize()
    # salary_df_copy = salary_df.copy()
    
    # salary_df_copy = salary_df_copy[
    #     (salary_df_copy['dt'] >= dt_from) &
    #     (salary_df_copy['dt'] <= dt_upto)
    # ]
    salary_df = salary_df.groupby(
        pd.Grouper(key='dt', freq=frequency)
    ).sum(numeric_only=True)
    salary_df.reset_index(inplace=True)
    
    all_dates = pd.date_range(start=dt_from, end=dt_upto, freq=frequency)
    all_dates_df = pd.DataFrame({ 'dt': all_dates })
    
    extended_salary_df = pd.merge(
        all_dates_df,
        salary_df,
        on='dt', how='left'
    )
    extended_salary_df['value'].fillna(0, inplace=True)
    
    formats = {
        'hour': "%Y-%m-%dT%H:00:00",
        'day': "%Y-%m-%dT00:00:00",
        'month': "%Y-%m-01T00:00:00"
    }
    extended_salary_df['dt'] = \
        extended_salary_df['dt'].dt.strftime(formats[group_type])
    
    data = {
        'dataset': extended_salary_df['value'].to_list(),
        'labels': extended_salary_df['dt'].to_list()
    }
    return data
