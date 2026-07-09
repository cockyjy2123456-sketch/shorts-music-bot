import os
import sys
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

if ".supabase.co" in SUPABASE_URL:
    SUPABASE_URL = SUPABASE_URL.split(".supabase.co")[0] + ".supabase.co"

api_url = f"{SUPABASE_URL}/rest/v1/songs"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def run_bot():
    print("🚀 ShortsTrend.io 봇이 데이터 타입을 교정하여 전송을 시도합니다...")
    
    # 💡 id 부분을 수열님의 테이블 타입(bigint)에 맞게 숫자로 전면 수정했습니다!
    collected_songs = [
        {
            "id": 1,  # 👈 숫자로 변경
            "title": "Night Dancer (Shorts Ver.)",
            "artist": "imase",
            "link": "https://youtube.com/shorts/OW0Mv8S6HNM?feature=share",
            "tags": ["#Japan", "#Chill"]
        },
        {
            "id": 2,  # 👈 숫자로 변경
            "title": "Cupid (Sped Up)",
            "artist": "FIFTY FIFTY",
            "link": "https://youtube.com/shorts/Qc7_zRjmzVs?feature=share",
            "tags": ["#Romance", "#SpeedUp"]
        }
    ]
    
    try:
        response = requests.post(api_url, headers=headers, json=collected_songs)
        
        if response.status_code in [200, 201]:
            print("✅ Supabase 데이터 갱신 완료! 전광판에 정상 저장되었습니다.")
        else:
            print(f"❌ Supabase 응답 에러 발생: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 네트워크 통신 자체 실패: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
