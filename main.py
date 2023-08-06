import requests
import json
import base64
import sys
from datetime import datetime


# 푼 문제가 지정한 난이도에 포함된다면 True, 아니면 False
def check_valid(platform, difficulty):
    if platform == '백준' and difficulty in ['Silver', 'Gold']:
        return True
    if platform == '프로그래머스' and difficulty in ['lv2']:
        return True
    if platform == 'SWEA' and difficulty in ['D4']:
        return True
    return False


# 가장 최근 커밋 내역을 파싱하여 스터디에 커밋할 난이도인지 체크
# 커밋 내역 객체를 입력받음
# 적절한 난이도라면 스터디 레포지터리에 커밋을 수행
def commit_if_valid(commit):
    for file in latest_commit['files']:
        # 파일 이름을 /를 구분자로 파싱해서 리스트에 담기
        full_filename = str(file['filename']).split('/')

        # 스터디에서 정한 난이도가 아닐 경우 커밋하지 않음
        # TODO: README도 같이 포함해서 올리도록 변경하기
        filename = full_filename[-1]
        if filename == 'README.md':
            continue

        platform = full_filename[0]
        difficulty = full_filename[1]

        # 커밋할 수 있는 난이도라면 커밋 과정 진행
        if check_valid(platform, difficulty):
            # 오늘 날짜를 yyyy.mm/dd 형식의 문자열로 저장
            date_string = datetime.now().strftime('%Y.%m/%d')

            commit_message = f'{platform} - {filename}'
            filename = f'{date_string}/{full_filename[-1]}'
            raw_code = requests.get(file['raw_url']).text
            # 문제풀이 코드를 base64로 인코딩
            base64_code = base64.b64encode(raw_code.encode()).decode('utf-8')

            request_body = {'message': commit_message, 'committer': {'name': nickname, 'email': email},
                           'author': {'name': nickname, 'email': email}, 'content': base64_code}

            # 커밋 생성 요청 보내기
            response = requests.put(
                f'https://api.github.com/repos/{nickname}/algostun/contents/{nickname}/{filename}',
                headers=headers, json=request_body)


# main 실행
# 환경변수 할당
(token, nickname, email, repository) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# HTTP Request 헤더 설정
headers = {'Authorization': f'Bearer {token}', 'X-GitHub-Api-Version': '2022-11-28',
           'accept': 'application/vnd.github+json'}

# 백준허브 연동 알고리즘 Repository의 커밋 목록을 불러옴
api_response = json.loads(requests.get(f'https://api.github.com/repos/{nickname}/{repository}/commits',
                                       headers=headers).text)[0]
# 커밋 API 응답으로부터 가장 최신 커밋을 불러옴
latest_commit = json.loads(requests.get(api_response['url'], headers=headers).text)

# 가장 최신 커밋으로부터 문제이름, 코드 추출
commit_if_valid(latest_commit)
