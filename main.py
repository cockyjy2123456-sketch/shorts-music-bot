import os
import sys
import requests
from googleapiclient.discovery import build

# 환경 변수 설정
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip('/')
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Supabase 연결 설정
supabase_url = f"{SUPABASE_URL}/rest/v1/songs"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def get_trending_shorts():
    # 유튜브 API를 통해 'Shorts' 관련 인기 영상 검색
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q="Shorts BGM trending",
        type="video",
        videoDuration="short",
        maxResults=5,
        order="viewCount"
    )
    response = request.execute()
    
    songs = []
    for item in response.get('items', []):
        # id 값을 제거하여 Supabase가 자동으로 생성하게 함 (데이터 누적용)
        song = {
            "title": item['snippet']['title'][:50],
            "artist": item['snippet']['channelTitle'],
            "link": f"https://www.youtube.com/shorts/{item['id']['videoId']}",
            "tags": "#Trending" 
        }
        songs.append(song)
    return songs

def run_bot():
    print("🚀 ShortsTrend.io 봇이 실시간 데이터를 수집합니다...")
    try:
        new_data = get_trending_shorts()
        
        print(f"DEBUG: 봇이 찾아온 데이터 개수: {len(new_data)}")
        
        if not new_data:
            print("⚠️ 경고: 유튜브에서 데이터를 하나도 못 찾아왔습니다.")
            return

        response = requests.post(supabase_url, headers=headers, json=new_data)
        
        if response.status_code in [200, 201, 204]:
            print("✅ Supabase 데이터 갱신 완료! 최신 곡들이 저장되었습니다.")
        else:
            print(f"❌ Supabase 에러: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 실패: {str(e)}")

if __name__ == "__main__":
    run_bot()
