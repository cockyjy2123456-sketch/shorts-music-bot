import os
import requests
from collections import Counter
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
    "Prefer": "resolution=ignore-duplicates" 
}

def get_trending_music():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    # 1. 트렌드 분석을 위해 100개 영상 수집
    request = youtube.search().list(
        part="snippet",
        q="trending shorts music viral audio",
        type="video",
        maxResults=100, 
        order="relevance"
    )
    response = request.execute()
    
    song_counts = Counter()
    song_details = {}

    for item in response.get('items', []):
        title = item['snippet']['title']
        
        # 필터링: 음악과 관련 없는 노이즈 제거
        if any(bad in title.lower() for bad in ['asmr', 'vlog', 'reaction', 'mukbang']):
            continue
        
        # 곡명 추출 (가장 깔끔하게 제목을 다듬기 위한 로직)
        clean_title = title.split('|')[0].split('-')[0].strip()
        
        # 빈도수 체크 및 세부 정보 저장
        song_counts[clean_title] += 1
        if clean_title not in song_details:
            song_details[clean_title] = {
                "title": clean_title,
                "artist": item['snippet']['channelTitle'],
                "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "tags": ["#Trending"]
            }
    
    # 2. 가장 많이 언급된 상위 5개 곡만 리턴
    top_5 = [song_details[title] for title, count in song_counts.most_common(5)]
    return top_5

def run_bot():
    print("🚀 수열님의 트렌드 BGM 봇 실행 중...")
    try:
        top_songs = get_trending_music()
        
        for song in top_songs:
            response = requests.post(supabase_url, headers=headers, json=song)
            if response.status_code in [200, 201]:
                print(f"✅ 저장 성공: {song['title']}")
            else:
                print(f"⏩ 이미 있는 곡 건너뜀: {song['title']}")
                
    except Exception as e:
        print(f"❌ 실패: {str(e)}")

if __name__ == "__main__":
    run_bot()
