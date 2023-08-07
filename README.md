# algostun-auto-commit

반복적이고 잊기 쉬운 알고리즘 스터디 커밋을 자동으로 해주는 스크립트입니다. 백준 허브를 이용하여 알고리즘 문제 풀이를 관리하고 있다면 자동으로 스터디 커밋 형식에 맞게 푼 문제 파일을 업로드 할 수 있습니다.

### 동작 방식

1. 플랫폼에서 문제를 풀 때마다 백준 허브로 관리하는 개인 레포지터리에 커밋된 가장 최근 내역을 읽어옵니다.
2. 파이썬 스크립트를 통해 읽어온 커밋 내역을 스터디의 커밋 컨벤션에 맞게 가공한 후 fork한 개인 algostun 레포지터리에 커밋합니다.

   ❗ 스터디에서 정한 범위 난이도는 풀이해도 커밋되지 않습니다.

   기준: 백준은 solved.ac기준 실버, 골드 난이도 / 프로그래머스는 Level 2 / SWEA는 D4

   ❗ 최근에 등록된 문제는 unrated로 분류되어 제대로 작동하지 않을 수 있습니다.

### 사용 방법

1.  아래의 스크립트를 복사하여 `{}`의 내용을 개인에 맞게 작성합니다.<br>
    - 최종적으로 `{}`는 없어야 합니다.<br>
    - `${{ }}`부분은 수정하면 안됩니다.
2.  작성한 yml파일을 백준 허브 연동 레포지터리의 .github/workflows 디렉토리 내에 추가합니다.<br>

    - yml파일의 이름은 상관없습니다.
      <br>

      ```YAML
      name: algostun_auto_commit
      on:
        push:
          branches:
            - 'main'
          paths:
            - '**.py'
            - '**.c'
            - '**.cpp'
            - '**.java'

      env:
        NICKNAME: {깃허브 닉네임}
        EMAIL: {깃허브 이메일}
        REPOSITORY: {백준 허브 연동 레포지터리}

      jobs:
        build:
          runs-on: ubuntu-latest

          steps:
            - uses: actions/checkout@v3
              with:
                repository: bmincof/algostun-auto-commit
                token: ${{ secrets.ACTIONS_KEY }}
            - run: ls

            - uses: actions/setup-python@v4
              with:
                python-version: '3.10'
                cache: 'pip' # caching pip dependencies
            - run: pip install -r requirements.txt
            - run: python main.py ${{ secrets.ACTIONS_KEY }} ${{ env.NICKNAME }} ${{ env.EMAIL }} ${{ env.REPOSITORY }}

      ```

3.  깃허브 레포지터리 내의 settings -> Secrets and variables -> Actions에 Repository secrets에 ACTIONS_KEY라는 이름으로 발급받은 Personal Access Token을 등록합니다.

### 프로젝트에 기여하는 방법

- 기능 추가 요청, 버그 제보 등은 Issues를 통해 남겨주시거나 fork 후 직접 수정하여 Pull Request 남겨주세요
- 그 외 코드 개선, 문서 수정 등의 작업은 fork 후 변경사항 Pull Request 남겨주세요
- 해당 프로젝트 기능 외의 스터디 편의를 위한 기능도 환영합니다
