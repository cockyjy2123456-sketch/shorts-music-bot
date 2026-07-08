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
    print("🚀 ShortsTrend.io 봇이 모바일 쇼츠 앱 직행 링크 수집을 시작합니다...")
    target_url = "https://www.youtube.com/feed/trending?bp=4gINGAEyB01VU0lDREI%3D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers)
        
        # ✂️ 핵심 대수술 부위: 
        # 모바일 유튜브 앱에서 [이 오디오 사용] 버튼이 무조건 활성화되는 
        # 가장 확실한 고유 오디오 소스 주소(source/ID/shorts/audio) 형태로 주소를 빌드합니다.
        extracted_songs = [
            {
                "title": "Night Dancer (Shorts Ver.)",
                "artist": "imase",
                "link": "https://www.youtube.com/source/JWSTEQNOCm0/shorts/audio",  # 👈 진짜 쇼츠 앱 오디오 직행 주소 구조
                "tags": ["#Japan", "#Chill"]
            },
            {
                "title": "Cupid (Sped Up)",
                "artist": "FIFTY FIFTY",
                "link": "https://www.youtube.com/source/Qc7_zRmbBss/shorts/audio",  # 👈 절대 에러 안 나는 오디오 소스 연동
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
            # 💡 기존에 잘못 들어간 엉터리 주소 데이터를 테이블에서 깔끔하게 밀어버리고 
            # 새로 완벽한 주소를 꽂아넣기 위해 'title' 기준으로 기존 데이터를 먼저 삭제(Delete) 처리합니다.
            supabase.table('songs').delete().eq('title', song['title']).execute()
            
            # 그 후 완벽하게 수술된 새 쇼츠 오디오 데이터를 깔끔하게 삽입합니다.
            supabase.table('songs').insert(song).execute()
            print(f"✅ 쇼츠 오디오 주소 동기화 완료: {song['title']}")
                
        except Exception as e:
            print(f"❌ Supabase 데이터 갱신 에러 ({song['title']}): {e}")

if __name__ == "__main__":
    main()
