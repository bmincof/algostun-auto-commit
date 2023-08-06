import requests
import json
import base64
import sys
from datetime import datetime

# 가장 최근에 커밋된 파일 이름을 파싱해서 반환
# 커밋 내역 객체를 입력받음
# 커밋 메시지, 난이도, 코드를 생성해서 반환
def parse_latest_commit(commit):
    for file in latest_commit['files']:
        # 파일 이름을 /를 구분자로 파싱해서 리스트에 담기
        full_filename = str(file['filename']).split('/')

        # 실버, 골드 난이도가 아닐 경우 커밋하지 않음
        # TODO: README도 나중에 같이 포함해서 올리도록 변경하기
        filename = full_filename[-1]
        if filename == 'README.md':
            continue

        difficulty = full_filename[1]
        if difficulty not in ['Silver', 'Gold']:
            return False

        # 오늘 날짜를 yyyy.mm/dd 형식의 문자열로 저장
        now = datetime.now().strftime('%Y.%m/%d')
        platform = full_filename[0]

        commit_message = f'{platform} - {filename}'
        filename = f'{now}/{full_filename[-1]}'
        code = requests.get(file['raw_url']).text
        # 문제풀이 코드를 base64로 인코딩
        encoded_code = base64.b64encode(code.encode()).decode('utf-8')

        return commit_message, filename, encoded_code


# 환경변수 할당
(token, nickname, email, repository) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# HTTP Request 헤더 설정
headers = {'Authorization': f'Bearer {token}', 'X-GitHub-Api-Version': '2022-11-28', 'accept': 'application/vnd.github+json'}

# 백준허브 연동 알고리즘 Repository의 커밋 목록을 불러옴
api_response = json.loads(requests.get(f'https://api.github.com/repos/{nickname}/{repository}/commits', headers=headers).text)[0]
# 커밋 API 응답으로부터 가장 최신 커밋을 불러옴
latest_commit = json.loads(requests.get(api_response['url'], headers=headers).text)

# 가장 최신 커밋으로부터 문제이름, 코드 추출
(commit_message, filename, encoded_code) = parse_latest_commit(latest_commit)
requestBody = {'message': commit_message, 'committer': {'name': nickname, 'email': email}, 'author': {'name': nickname, 'email': email}, 'content': encoded_code }

# 커밋 생성 요청 보내기
response = requests.put(f'https://api.github.com/repos/{nickname}/algostun/contents/{nickname}/{filename}', headers=headers, json=requestBody )
print(response)
