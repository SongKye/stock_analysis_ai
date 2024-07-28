
import logger
import datetime

import sys
import os
# 현재 스크립트가 있는 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)
import DartAPI_utils as DU

def get_stock_info_api(name, code='11011'):
    if code == '11011':
        return DU.remake_df_4Q(name, code)
    elif code == '11012':
        return DU.remake_df_1Q_2Q_3Q(name, code)
    elif code == '11013':
        return DU.remake_df_1Q_2Q_3Q(name, code)
    elif code == '11014':
        return DU.remake_df_1Q_2Q_3Q(name, code)
    else:
        logger.error(f"reprt_code error")

if __name__== "__main__":
    get_stock_info_api("005930", code='11012')  # 이름이 아닌 code로 가져오는게 안전함

