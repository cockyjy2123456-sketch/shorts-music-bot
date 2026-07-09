import os
import requests

# 🔐 깃허브 환경변수에서 안전하게 주소와 키를 가져옵니다.
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# 🎯 오류(PGRST125) 방지를 위해 정확한 REST API URL 주소를 조립합니다.
# 주소 뒤에 /rest/v1/songs가 깔끔하게 붙어야 에러가 나지 않습니다.
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"  # 중복 데이터는 덮어쓰기 설정
}

def run_bot():
    print("🚀 ShortsTrend.io 봇이 브라우저 이탈 방지용 쇼츠 피드 링크 수집을 시작합니다...")
    
    # 🎵 유튜브에서 수집해 온 가상의 데이터 샘플 (실제 크롤링 코드에 맞게 유지)
    collected_songs = [
        {
            "id": "song_001",
            "title": "Night Dancer (Shorts Ver.)",
            "artist": "imase",
            "link": "https://youtube.com/shorts/OW0Mv8S6HNM?feature=share",
            "tags": ["#Japan", "#Chill"]
        },
        {
            "id": "song_002",
            "title": "Cupid (Sped Up)",
            "artist": "FIFTY FIFTY",
            "link": "https://youtube.com/shorts/Qc7_zRjmzVs?feature=share",
            "tags": ["#Romance", "#SpeedUp"]
        }
    ]
    
    # ⚡ 수열님의 Supabase 테이블에 데이터 밀어넣기
    api_url = f"{SUPABASE_URL}/rest/v1/songs"
    
    response = requests.post(api_url, headers=headers, json=collected_songs)
    
    if response.status_code in [200, 201]:
        print("✅ Supabase 데이터 갱신 완료! 성공적으로 전광판에 저장되었습니다.")
    else:
        print(f"❌ Supabase 데이터 갱신 실패: {response.text}")

if __name__ == "__main__":
    run_bot()
