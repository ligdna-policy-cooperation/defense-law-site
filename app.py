import streamlit as st
import glob
import xml.etree.ElementTree as ET
import pandas as pd

# 1. 사이트 기본 설정
st.set_page_config(page_title="방위산업 법령 검색 AI", page_icon="🛡️", layout="wide")

st.title("🛡️ 방위산업 최신 법령 AI 검색기")
st.write("매일 업데이트되는 방위산업 관련 법령을 확인하고, AI에게 질문해보세요!")

# 2. 사이드바 (왼쪽 메뉴)
st.sidebar.header("📂 수집된 최신 법령 파일")
xml_files = glob.glob("*.xml")
if xml_files:
    for file in xml_files:
        st.sidebar.success(file)
else:
    st.sidebar.warning("아직 수집된 법령 파일이 없습니다.")

# =====================================================================
# ⭐ 새롭게 추가된 부분: 최근 개정 사항 요약표 만들기
# =====================================================================
st.subheader("📢 최근 개정 사항 및 시행 일정")

update_list = [] # 데이터를 담을 빈 바구니

# 폴더에 있는 XML 파일들을 하나씩 열어서 개정 정보만 쏙쏙 뽑아옵니다.
if xml_files:
    for file in xml_files:
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            
            # 법령 목록 중 첫 번째(가장 최신) 정보 가져오기
            law = root.find("law")
            if law is not None:
                name = law.findtext("법령명한글")
                status = law.findtext("현행연혁코드") # 예: 현행, 시행예정
                date = law.findtext("시행일자")       # 예: 20261210
                type_ = law.findtext("제개정구분명")  # 예: 일부개정, 타법개정
                
                # 보기 좋게 데이터 정리하기
                update_list.append({
                    "법령명": name,
                    "상태": status,
                    "시행일자": f"{date[:4]}년 {date[4:6]}월 {date[6:]}일",
                    "개정구분": type_
                })
        except:
            pass # 에러가 나면 사이트가 안 꺼지게 조용히 넘어갑니다.

# 뽑아온 데이터가 있다면 예쁜 표(Dataframe)로 화면에 그립니다.
if update_list:
    df = pd.DataFrame(update_list)
    # 인덱스(번호)를 숨기고 넓게 표시
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("수집된 법령 데이터가 없거나 분석할 수 없습니다.")

st.divider() # 깔끔하게 가로선 긋기
# =====================================================================

# 3. 챗봇 대화창 UI
st.subheader("💬 법령 AI 챗봇 (두뇌 이식 준비 중)")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 방위사업법, 군수품관리법 등 궁금한 내용을 물어보세요."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("질문을 입력하세요 (예: 최근 개정된 방위사업법 내용이 뭐야?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        st.markdown("*(로딩중... 실제 AI 연동과 법안 해석은 다음 단계에서 진행됩니다!)*")
