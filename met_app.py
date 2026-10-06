import requests
import streamlit as st

# 1. API 엔드포인트 설정
SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

# 2. 검색어에 맞는 작품 ID 목록 가져오기 (1시간 캐싱)
@st.cache_data(ttl=3600)
def search_ids(query, limit):
    resp = requests.get(
        SEARCH_URL,
        params={"q": query, "hasImages": "true", "limit": limit},
        timeout=10,
    )
    resp.raise_for_status()
    # 검색 결과가 없을 경우 null을 반환할 수 있으므로 [] 사용
    return resp.json().get("objectIDs") or []

# 3. 개별 작품의 상세 정보 가져오기 (1시간 캐싱)
@st.cache_data(ttl=3600)
def get_object(object_id):
    resp = requests.get(f"{OBJECT_URL}/{object_id}", timeout=10)
    resp.raise_for_status()
    return resp.json()

# 4. Streamlit UI 구성
st.set_page_config(page_title="Explore Artworks", layout="centered")
st.title("Explore Artworks with the MET Museum API")
st.caption("Arts and Advanced Big Data | Open API, Service 1")

# 사용자 입력 받기
query = st.text_input("Search for Artworks", "flower")
count = st.slider("How many artworks to show", 3, 12, 6)

# 검색 실행 및 결과 표시
if query.strip():
    try:
        ids = search_ids(query.strip(), count)
        if not ids:
            st.info("No artworks found. Try another word, for example: cat, ocean, gold.")
        else:
            cols = st.columns(3)
            for i, object_id in enumerate(ids):
                art = get_object(object_id)
                image = art.get("primaryImageSmall")
                
                # 이미지가 없으면 건너뜀
                if not image:
                    continue
                
                # 3개의 열에 순서대로 배치
                with cols[i % 3]:
                    st.image(image, width="stretch")
                    st.markdown(f"**{art.get('title', 'Untitled')}**")
                    st.write(f"Artist: {art.get('artistDisplayName') or 'Unknown'}")
                    st.write(f"Year: {art.get('objectDate') or 'Unknown'}")
                    if art.get("objectURL"):
                        st.markdown(f"[View at the Met]({art['objectURL']})")
                        
    except requests.RequestException:
        st.error("Could not reach the museum's service right now. Please try again in a minute.")

st.caption("Data: The Metropolitan Museum of Art Collection API (Open Access, CC0).")
