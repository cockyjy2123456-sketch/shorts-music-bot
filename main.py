import os
import requests
from googleapiclient.discovery import build

# 환경 변수 설정
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip('/')
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

supabase_url = f"{SUPABASE_URL}/rest/v1/songs"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

def get_pure_music_trending():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    # 1. 음악 카테고리(10)로 강제 지정하고 검색
    # 쇼츠 관련 키워드를 제외한 순수 음악 차트/바이럴 음악 검색
    request = youtube.search().list(
        part="snippet",
        q="viral trending pop songs 2026",
        type="video",
        videoCategoryId="10", 
        maxResults=20,
        order="viewCount"
    )
    response = request.execute()
    
    music_list = []
    for item in response.get('items', []):
        title = item['snippet']['title']
        
        # 2. 쇼츠, 리액션 등 음악 본질을 해치는 영상 강제 배제
        excluded = ['shorts', 'tiktok', 'reels', 'reaction', 'vlog', 'asmr']
        if any(word in title.lower() for word in excluded):
            continue
            
        # 3. 데이터 구조화 (음악 감상 페이지 링크로 저장)
        music_data = {
            "title": title.split('-')[0].strip(), # 곡명 위주로 깔끔하게 처리
            "artist": item['snippet']['channelTitle'].replace(' - Topic', ''),
            "link": f"https://music.youtube.com/watch?v={item['id']['videoId']}", # 음악 전용 플레이어
            "tags": ["#Trending"]
        }
        music_list.append(music_data)
        
        if len(music_list) >= 5:
            break
            
    return music_list

def run_bot():
    try:
        top_music = get_pure_music_trending()
        for song in top_music:
            response = requests.post(supabase_url, headers=headers, json=song)
            if response.status_code in [200, 201]:
                print(f"✅ 추가 완료: {song['title']}")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    run_bot()
