import streamlit as st
import glob
import os

# 1. 사이트 기본 설정 (이름, 아이콘, 넓은 화면)
st.set_page_config(page_title="방위산업 법령 검색 AI", page_icon="🛡️", layout="wide")

# 2. 메인 타이틀
st.title("🛡️ 방위산업 최신 법령 AI 검색기")
st.write("매일 업데이트되는 방위산업 관련 법령을 확인하고, AI에게 질문해보세요!")

# 3. 사이드바 (왼쪽 메뉴) 만들기
st.sidebar.header("📂 수집된 최신 법령 파일")

# 깃허브에 같이 올라와 있는 xml 파일들을 찾아서 보여줍니다.
xml_files = glob.glob("*.xml")
if xml_files:
    for file in xml_files:
        st.sidebar.success(file)
else:
    st.sidebar.warning("아직 수집된 법령 파일이 없습니다.")

st.sidebar.info("💡 추후 이곳에 '신구대조표' 시각화 기능이 추가될 예정입니다.")

# 4. 챗봇 대화창 UI 마법
st.subheader("💬 법령 AI 챗봇 (디자인 테스트)")

# 대화 기록을 저장하는 메모장 역할
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 방위사업법, 군수품관리법 등 궁금한 내용을 물어보세요."}]

# 이전 대화 내용들을 화면에 뿌려주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자가 입력할 수 있는 채팅창
if prompt := st.chat_input("질문을 입력하세요 (예: 최근 개정된 방위사업법 내용이 뭐야?)"):
    # 사용자의 질문을 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI의 가짜 답변 (진짜 AI는 다음 단계에서 연결합니다)
    with st.chat_message("assistant"):
        st.markdown("*(로딩중... 실제 AI 연동과 법안 해석은 다음 개발 단계에서 진행됩니다!)*")
