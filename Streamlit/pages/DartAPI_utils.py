
import OpenDartReader
import pandas as pd

api_key = 'c49a57e08d86f3eadd001281cfdf95865549056b'
dart = OpenDartReader(api_key)

# reprt_code
map_code_quater = {
    '11011' : '사업보고서',
    '11013' : '1분기 보고서',
    '11012' : '반기 보고서',
    '11014' : '3분기 보고서',
}

def remake_df_1Q_2Q_3Q(name, code):
    df_table = {}
    data = dart.finstate_all(name, 2023, reprt_code=code)
    df = pd.DataFrame(data)

    columns_to_save = [
        'account_nm', 'sj_nm', 
        'thstrm_nm', 'thstrm_amount', 'thstrm_add_amount', 
        'frmtrm_nm', 'frmtrm_amount', 
        'frmtrm_q_nm', 'frmtrm_q_amount', 'frmtrm_add_amount']
    df_selected = df[columns_to_save]

    # sj_nm 값을 기준으로 데이터프레임 분류
    sj_nm_values = df_selected['sj_nm'].unique()

    for sj_nm_value in sj_nm_values:
        subset_df = df_selected[df_selected['sj_nm'] == sj_nm_value].reset_index(drop=True)

        new_columns = {}
        # 재구성할 열 이름과 값 매핑
        if sj_nm_value == '재무상태표':
            new_columns = {
                'thstrm_nm': 'thstrm_amount',
                'frmtrm_nm': 'frmtrm_amount',
            }
        else:
            new_columns = {
                'thstrm_nm': ['thstrm_amount', 'thstrm_add_amount'],
                'frmtrm_q_nm': ['frmtrm_q_amount' , 'frmtrm_add_amount'],
            }

        # 새로운 데이터프레임 생성
        restructured_data = {
            'account_nm': subset_df['account_nm'].tolist(),
        }

        if sj_nm_value == '재무상태표':
                # 각 기간에 대한 데이터를 재구성
            for period_col, amount_col in new_columns.items():
                period_data = {}
                for i, period in enumerate(subset_df[period_col]):
                    if period not in period_data:
                        period_data[period] = [None] * len(subset_df)
                    period_data[period][i] = subset_df.at[i, amount_col]

                for period, amounts in period_data.items():
                    if period not in restructured_data:
                        restructured_data[period] = amounts
                    else:
                        restructured_data[period] = [
                            amount if amount is not None else restructured_data[period][i] 
                            for i, amount in enumerate(amounts)
                        ]

            # 재구성된 데이터로 새로운 데이터프레임 생성
            restructured_df = pd.DataFrame(restructured_data)

            # CSV 파일로 저장
            # csv_file_path = f'{name}__{map_code_quater[code]}_{sj_nm_value}_output.csv'
            # restructured_df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        else:
            # 각 기간에 대한 데이터를 재구성
            for period_col, amount_cols in new_columns.items():
                if period_col not in subset_df.columns:
                    continue

                for amount_col in amount_cols:
                    period_data = {}
                    for i, period in enumerate(subset_df[period_col]):
                        if period is None or pd.isna(period):
                            continue
                        
                        column_name = f"{period} 누적" if 'add_amount' in amount_col else period

                        if column_name not in period_data:
                            period_data[column_name] = [None] * len(subset_df)
                        
                        # amount_col이 실제로 subset_df에 존재하는지 확인
                        if amount_col in subset_df.columns:
                            period_data[column_name][i] = subset_df.at[i, amount_col]
                        else:
                            period_data[column_name][i] = None

                    for column_name, amounts in period_data.items():
                        if column_name not in restructured_data:
                            restructured_data[column_name] = amounts
                        else:
                            restructured_data[column_name] = [
                                amount if amount is not None else restructured_data[column_name][i]
                                for i, amount in enumerate(amounts)
                            ]

            restructured_df = pd.DataFrame(restructured_data)
    
        df_table[sj_nm_value] = restructured_df

    return df_table

def remake_df_4Q(name, code):
    data = dart.finstate_all(name, 2023, reprt_code=code)
    df = pd.DataFrame(data)

    columns_to_save = ['account_nm', 'sj_nm', 'thstrm_nm', 'thstrm_amount', 'frmtrm_nm', 'frmtrm_amount', 'bfefrmtrm_nm', 'bfefrmtrm_amount']
    df_selected = df[columns_to_save]

    # 재구성할 열 이름과 값 매핑
    new_columns = {
        'thstrm_nm': 'thstrm_amount',
        'frmtrm_nm': 'frmtrm_amount',
        'bfefrmtrm_nm': 'bfefrmtrm_amount'
    }

    # 결과를 저장할 딕셔너리
    df_table = {}

    # sj_nm 값을 기준으로 데이터프레임 분류
    sj_nm_values = df_selected['sj_nm'].unique()

    for sj_nm_value in sj_nm_values:
        subset_df = df_selected[df_selected['sj_nm'] == sj_nm_value].reset_index(drop=True)

        # 새로운 데이터프레임 생성
        restructured_data = {
            'account_nm': subset_df['account_nm']
        }

        for period_col, amount_col in new_columns.items():
            for i, period in enumerate(subset_df[period_col]):
                if period not in restructured_data:
                    restructured_data[period] = []
                restructured_data[period].append(subset_df.at[i, amount_col])

        restructured_df = pd.DataFrame(restructured_data)

        # 결과를 딕셔너리에 저장
        df_table[sj_nm_value] = restructured_df

    return df_table

    csv_file_path = f'{name}_{map_code_quater[code]}_output.csv'
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')