
import OpenDartReader
import pandas as pd

api_key = 'c49a57e08d86f3eadd001281cfdf95865549056b'
dart = OpenDartReader(api_key)

def get_stock_info_api(name):
    data = dart.finstate(name, 2023)
    df = pd.DataFrame(data)

    columns_to_save = ['account_nm', 'thstrm_nm', 'thstrm_amount', 'frmtrm_nm', 'frmtrm_amount', 'bfefrmtrm_nm', 'bfefrmtrm_amount']
    df_selected = df[columns_to_save]

    # 재구성할 열 이름과 값 매핑
    new_columns = {
        'thstrm_nm': 'thstrm_amount',
        'frmtrm_nm': 'frmtrm_amount',
        'bfefrmtrm_nm': 'bfefrmtrm_amount'
    }

    # 새로운 데이터프레임 생성
    restructured_data = {'account_nm': df_selected['account_nm']}

    for period_col, amount_col in new_columns.items():
        for i, period in enumerate(df[period_col]):
            if period not in restructured_data:
                restructured_data[period] = []
            restructured_data[period].append(df.at[i, amount_col])

    restructured_df = pd.DataFrame(restructured_data)
    return restructured_df

    # csv_file_path = 'dataframe_output.csv'
    # restructured_df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

if __name__== "__main__":
    get_stock_info_api("삼성전자")

