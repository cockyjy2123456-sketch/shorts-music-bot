import os
from googleapiclient.discovery import build
from supabase import create_client

# 설정 불러오기
youtube = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY'))
supabase = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_KEY'))

# 예시: 봇이 정상 작동하는지 확인하는 코드
print("봇이 정상적으로 시작되었습니다!")
