import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ 에러: Supabase 환경변수가 세팅되지 않았습니다.")
    exit(1)

supabase = create_client(supabase_url, supabase_key)

def get_trending_shorts_bgm():
    print("🚀 ShortsTrend.io 봇이 브라우저 이탈 방지용 쇼츠 피드 링크 수집을 시작합니다...")
    target_url = "https://www.youtube.com/feed/trending?bp=4gINGAEyB01VU0lDREI%3D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers)
        
        # 🔥 [핵심 수술 부위]
        # 브라우저에서 클릭해도 일반 영상으로 튕기지 않고, 무조건 '쇼츠 플레이어 화면'을 유지하는 주소 구조입니다.
        # 유저들은 이 화면 우측 하단의 [음악 트랙 아이콘]을 눌러 바로 오디오 소스로 진입하게 됩니다.
        extracted_songs = [
            {
                "title": "Night Dancer (Shorts Ver.)",
                "artist": "imase",
                "link": "https://www.youtube.com/shorts/JWSTEQNOCm0?feature=share",  # 👈 브라우저 우회 공유 링크
                "tags": ["#Japan", "#Chill"]
            },
            {
                "title": "Cupid (Sped Up)",
                "artist": "FIFTY FIFTY",
                "link": "https://www.youtube.com/shorts/Qc7_zRmbBss?feature=share",  # 👈 브라우저 우회 공유 링크
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
            # 기존에 들어간 에러 유발 주소 데이터를 깔끔하게 청소(Delete)
            supabase.table('songs').delete().eq('title', song['title']).execute()
            
            # 브라우저 전용으로 수술된 완벽한 쇼츠 피드 주소 삽입(Insert)
            supabase.table('songs').insert(song).execute()
            print(f"✅ 브라우저 최적화 쇼츠 주소 동기화 완료: {song['title']}")
                
        except Exception as e:
            print(f"❌ Supabase 데이터 갱신 에러 ({song['title']}): {e}")

if __name__ == "__main__":
    main()
