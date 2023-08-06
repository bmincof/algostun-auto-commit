import requests
import json
import base64
import sys
from datetime import datetime

# 환경변수 할당
(token, nickname, email, repository) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# HTTP Request 헤더 설정
headers = {'Authorization': f'Bearer {token}', 'X-GitHub-Api-Version': '2022-11-28', 'accept': 'application/vnd.github+json'}

# 백준허브 연동 알고리즘 Repository의 커밋 목록을 불러옴
api_response = json.loads(requests.get(f'https://api.github.com/repos/{nickname}/{repository}/commits', headers=headers).text)[0]
# 커밋 API 응답으로부터 가장 최신 커밋을 불러옴
latest_commit = json.loads(requests.get(api_response['url'], headers=headers).text)

# 가장 최신 커밋으로부터 문제이름, 코드 추출
platform = ''
difficulty = ''
filename = ''
code = ''

# 파일 이름 파싱하기
for file in latest_commit['files']:
    full_filename = str(file['filename']).split('/')
    if full_filename[-1] == 'README.md':
        continue

    now = datetime.now().strftime('%Y.%m/%d')
    platform = full_filename[0]
    difficulty = full_filename[1]
    filename = f'{now}/{full_filename[-1]}'
    code = requests.get(file['raw_url']).text

# 실버 / 골드 난이도를 해결했을 때만 커밋
if difficulty in ['Silver', 'Gold']:
    commit_message = f'{platform} - {filename}'
    # filename과 code로 커밋할 파일 만들기
    encoded_code = base64.b64encode(code.encode()).decode('utf-8')
    requestBody = {'message': commit_message, 'committer': {'name': {nickname}, 'email': {email}}, 'author': {'name': {nickname}, 'email': {email}}, 'content': encoded_code }

    # 파일명 규칙 작성자/yyyy.mm/dd/
    response = requests.put(f'https://api.github.com/repos/{nickname}/algostun/contents/{nickname}/{filename}', headers=headers, json=requestBody )
    print(response.text)
