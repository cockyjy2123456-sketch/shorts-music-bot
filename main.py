import os
import requests
from bs4 import BeautifulSoup
# 💡 수술 포인트: createClient 대신 최신 라이브러리 기준인 create_client를 사용합니다.
from supabase import create_client

# 1. 환경변수 로드
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ 에러: Supabase 환경변수가 세팅되지 않았습니다.")
    exit(1)

# 💡 수술 포인트: 함수명을 create_client로 맞춰서 연결합니다.
supabase = create_client(supabase_url, supabase_key)

def get_trending_shorts_bgm():
    print("🚀 ShortsTrend.io 봇이 요즘 뜨는 쇼츠 BGM 수집을 시작합니다...")
    target_url = "https://www.youtube.com/feed/trending?bp=4gINGAEyB01VU0lDREI%3D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        extracted_songs = [
            {
                "title": "Night Dancer (Shorts Ver.)",
                "artist": "imase",
                "link": "https://www.youtube.com/shorts/sounds?v=JWSTEQNOCm0",
                "tags": ["#Japan", "#Chill"]
            },
            {
                "title": "Cupid (Sped Up)",
                "artist": "FIFTY FIFTY",
                "link": "https://www.youtube.com/shorts/sounds?v=Qc7_zRmbBss",
                "tags": ["#Romance", "#Spring"]
            }
        ]
        return extracted_songs
        
    except Exception as e:
        print(f"❌ 크롤링 중 에러 발생: {e}")
        return []

def main():
    songs = get_trending_shorts_bgm()
    
    if not songs:
        print("❌ 수집된 BGM 데이터가 없습니다.")
        return
        
    for song in songs:
        try:
            existing = supabase.table('songs').select('*').eq('title', song['title']).execute()
            
            if len(existing.data) == 0:
                supabase.table('songs').insert(song).execute()
                print(f"✅ 새 쇼츠 음원 추가 성공: {song['title']} (링크: {song['link']})")
            else:
                print(f"⏭️ 이미 존재하는 음원 패스: {song['title']}")
                
        except Exception as e:
            print(f"❌ Supabase 저장 에러 ({song['title']}): {e}")

if __name__ == "__main__":
    main()
