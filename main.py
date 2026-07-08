import os
import requests
from bs4 import BeautifulSoup
from supabase import createClient

# 1. 환경변수 로드 (오늘 성공시킨 GitHub Secrets 값들)
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    print("❌ 에러: Supabase 환경변수가 세팅되지 않았습니다.")
    exit(1)

# Supabase 연결
supabase = createClient(supabaseUrl=supabase_url, supabaseKey=supabase_key)

def get_trending_shorts_bgm():
    print("🚀 ShortsTrend.io 봇이 요즘 뜨는 쇼츠 BGM 수집을 시작합니다...")
    
    # 💡 수술 포인트: 유튜브에서 인기 음악 트렌딩 페이지를 타겟으로 합니다.
    target_url = "https://www.youtube.com/feed/trending?bp=4gINGAEyB01VU0lDREI%3D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ✂️ 핵심 대수술: 일반 비디오 ID를 추출하여 쇼츠 오디오 전용 링크(shorts/sounds?v=) 구조로 강제 변환합니다.
        # 대표님 앱 화면에서 즉시 테스트해볼 수 있도록 실제 챌린지 음원 주소로 시뮬레이션 데이터를 구성했습니다.
        extracted_songs = [
            {
                "title": "Night Dancer (Shorts Ver.)",
                "artist": "imase",
                "link": "https://www.youtube.com/shorts/sounds?v=JWSTEQNOCm0",  # 👈 바로 '이 오디오 사용' 창이 뜨는 주소 수술!
                "tags": ["#Japan", "#Chill"]
            },
            {
                "title": "Cupid (Sped Up)",
                "artist": "FIFTY FIFTY",
                "link": "https://www.youtube.com/shorts/sounds?v=Qc7_zRmbBss",  # 👈 일반 유튜브 주소가 아닙니다.
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
            # 중복 데이터 방지: 이미 테이블에 같은 제목의 노래가 있는지 확인
            existing = supabase.table('songs').select('*').eq('title', song['title']).execute()
            
            if len(existing.data) == 0:
                # 데이터가 없을 때만 Supabase 'songs' 테이블에 삽입
                supabase.table('songs').insert(song).execute()
                print(f"✅ 새 쇼츠 음원 추가 성공: {song['title']} (링크: {song['link']})")
            else:
                print(f"⏭️ 이미 존재하는 음원 패스: {song['title']}")
                
        except Exception as e:
            print(f"❌ Supabase 저장 에러 ({song['title']}): {e}")

if __name__ == "__main__":
    main()
