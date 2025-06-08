import streamlit as st
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import time

st.set_page_config(page_title="TrendSeller 데모", layout="wide")
st.title("🔥 TrendSeller: 쿠팡 & 유튜브 인기 제품 리뷰 탐색기")

keyword = st.text_input("🔍 검색할 제품 키워드 입력", value="폼롤러")

def crawl_coupang_best(keyword):
    url = f"https://www.coupang.com/np/search?q={keyword}&channel=user"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("ul.search-product-list li.search-product")
    result = []
    for product in products[:5]:
        title = product.select_one("div.name")
        price = product.select_one("strong.price-value")
        link = product.select_one("a")
        if title and price and link:
            result.append({
                "title": title.text.strip(),
                "price": price.text.strip(),
                "link": "https://www.coupang.com" + link['href']
            })
    return result

def search_youtube_videos(keyword):
    API_KEY = "AIzaSyBOjbAJSGP02mrurAF_YZzEpI8AnA7rv9o"
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.search().list(
        q=keyword + " 리뷰",
        part="snippet",
        type="video",
        maxResults=5,
        order="viewCount",
        relevanceLanguage="ko"
    )
    response = request.execute()
    results = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        results.append({"title": title, "url": url})
    return results

if st.button("🔥 인기 상품 & 영상 불러오기"):
    with st.spinner("데이터 수집 중..."):
        st.write("✅ 버튼 클릭됨")
        time.sleep(1)

        try:
            st.write("🛒 쿠팡 수집 시작")
            coupang_results = crawl_coupang_best(keyword)
            st.subheader("🛒 쿠팡 인기 상품")
            for item in coupang_results:
                st.markdown(f"**{item['title']}**  
가격: {item['price']}원  
[구매 링크]({item['link']})")
                st.markdown("---")
        except Exception as e:
            st.error("❌ 쿠팡 상품 수집 실패")
            st.code(str(e))

        try:
            st.write("🎬 유튜브 수집 시작")
            youtube_results = search_youtube_videos(keyword)
            st.subheader("🎬 유튜브 인기 리뷰 영상")
            for video in youtube_results:
                st.markdown(f"**{video['title']}**  
[영상 보기]({video['url']})")
                st.markdown("---")
        except Exception as e:
            st.error("❌ 유튜브 영상 수집 실패")
            st.code(str(e))
