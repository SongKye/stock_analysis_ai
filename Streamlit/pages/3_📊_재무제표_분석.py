import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

import sys
import os
# 현재 스크립트가 있는 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from DartAPI_manager import get_stock_info_api

st.set_page_config(page_title="재무제표 분석", page_icon="📊")

st.markdown("# 재무제표 분석")
st.sidebar.header("재무제표 분석")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)

# 버튼들을 한 행에 배치
col1, col2, col3, col4 = st.columns(4)

# 세션 상태 초기화
if 'quarter' not in st.session_state:
    st.session_state['quarter'] = '11011'

with col1:
    if st.button('1분기'):
        st.session_state['quarter'] = '11013'

with col2:
    if st.button('2분기'):
        st.session_state['quarter'] = '11012'

with col3:
    if st.button('3분기'):
        st.session_state['quarter'] = '11014'

with col4:
    if st.button('4분기'):
        st.session_state['quarter'] = '11011'

# 텍스트 입력 칸을 만들고 사용자가 입력한 값을 변수에 저장
user_input = st.text_input("Enter some text:")

def get_stock_data():
    if user_input is not None:
       return get_stock_info_api(user_input, code=st.session_state['quarter'])
    
if st.button('Click Me'):
    data = get_stock_data()
    # data가 dict인지 확인
    if isinstance(data, dict):
        for key, df in data.items():
            st.write(f"### {key}")
            st.write(df)
        

if __name__== "__main__":
    pass
   