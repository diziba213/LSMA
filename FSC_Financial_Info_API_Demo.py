import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import matplotlib as mpl
import xml.etree.ElementTree as ET

# 한글 폰트 설정 (예: 나눔고딕)
mpl.rc('font', family='NanumGothic')

# CORPCODE.xml 파일 경로 (대문자로 수정)
CORP_CODE_PATH = './CORPCODE.xml'

# Streamlit 페이지 제목
st.title("금융위원회_기업 재무 정보 조회")

# XML 파일에서 회사명 검색 함수
def search_company_name(search_name):
    tree = ET.parse(CORP_CODE_PATH)
    root = tree.getroot()
    results = []

    for list_element in root.findall("list"):
        corp_name = list_element.find("corp_name").text.strip()
        if search_name in corp_name:
            corp_code = list_element.find("corp_code").text.strip()
            stock_code = list_element.find("stock_code").text.strip() if list_element.find("stock_code").text else "N/A"
            jurir_no = list_element.find("jurir_no").text.strip() if list_element.find("jurir_no") is not None else "N/A"
            results.append((corp_code, corp_name, stock_code, jurir_no))
    
    return results

# 사용자 입력 받기
search_name = st.text_input("조회할 회사명을 입력하세요:")

if search_name:
    search_results = search_company_name(search_name)
    if search_results:
        st.write(f"검색 결과: {len(search_results)}개의 회사가 발견되었습니다.")
        
        # 검색 결과 표시 및 선택
        company_selection = st.selectbox(
            "회사를 선택하세요:",
            [(f"{name} (종목코드: {stock})", code, jurir) for code, name, stock, jurir in search_results]
        )
        
        if company_selection:
            corp_code, company_name, jurir_no = [item[1:] for item in search_results if item[0] in company_selection][0]
            st.write(f"선택된 회사명: {company_name}")
            st.write(f"법인등록번호 (jurir_no): {jurir_no}")
            
            if jurir_no == "N/A":
                st.warning("해당 회사의 법인등록번호(jurir_no)가 존재하지 않습니다. 다른 회사를 선택하거나 확인해 주세요.")
            else:
                # 금융위원회 API 요청 함수
                def get_financial_data(jurir_no, year):
                    url = "https://apis.data.go.kr/1160100/service/GetFinaStatInfoService_V2/getSummFinaStat_V2"
                    params = {
                        "serviceKey": "L8shibp7+lod8AboRbcSeMEiNGV7hGwZlH73UR00d7nOz5DIFIry807raa5tU1a663XmNC36ug9nhpaWIBHfcw==",
                        "crno": jurir_no,
                        "bizYear": str(year),
                        "numOfRows": "100",
                        "pageNo": "1",
                        "resultType": "json"
                    }
                    response = requests.get(url, params=params)
                    
                    if response.status_code == 200:
                        try:
                            return response.json()
                        except requests.exceptions.JSONDecodeError:
                            st.error(f"API 응답 오류 (연도: {year}) - JSON 형식이 아님. 응답 내용: {response.text}")
                            return None
                    else:
                        st.error(f"API 요청 오류 (연도: {year}) - HTTP 상태 코드: {response.status_code}")
                        return None
