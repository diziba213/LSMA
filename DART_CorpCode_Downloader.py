import requests
import zipfile
import os

# DART API 인증키 설정
API_KEY = "3d5ef17014755b107511ccf5c3b083b553dc2518"

# corpCode.xml 파일 저장 경로 설정
output_dir = "./"
output_zip_path = os.path.join(output_dir, "corpCode.zip")
output_xml_path = os.path.join(output_dir, "corpCode.xml")

# API URL 설정
url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"

# 데이터 요청
try:
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_zip_path, "wb") as file:
            file.write(response.content)
        print("✅ API 요청 성공! corpCode.zip 파일 다운로드 완료.")
    else:
        print(f"❌ API 요청 실패. 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        exit()
except Exception as e:
    print(f"❌ 요청 오류 발생: {e}")
    exit()

# 압축 해제
try:
    with zipfile.ZipFile(output_zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"✅ 압축 해제 완료. 파일 저장 경로: {output_xml_path}")
except Exception as e:
    print(f"❌ 압축 해제 오류: {e}")
    exit()

# 다운로드된 ZIP 파일 삭제 (선택 사항)
try:
    os.remove(output_zip_path)
    print("✅ ZIP 파일 삭제 완료.")
except Exception as e:
    print(f"❌ ZIP 파일 삭제 오류: {e}")
