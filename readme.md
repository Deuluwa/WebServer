# 웹서버 정보
## Django 사양
* Python 3.7
* Django 2.1.1

 ## 개발 툴
* PyCharm Professional(개발), VisualStudio 2017(버전관리 및 디버깅)

# 왜 Django? (왜 Python?)
* 웹개발은 생판 처음.
* Java, jsp를 하면 좋겠지만, 현업(Application 개발) 종사, 현재 프로젝트도 Xamarin이 주기때문에 시간 투자가 쉽지 않음.
* RestAPI만 사용하고 관리자페이지는 시간이 모자라면 개발을 못해도 상관 없음.
* 하지만 파이썬은 체득이 가능.
* 파이썬으로 여러 분야에 활용이 가능하리라 판단.

# 개발 예정 사항
* **Xamarin 어플리케이션과 통신할수 있는 RestAPI**
  * 로그인
  * 사용자 정보
  * 수업정보
  * 출석정보
  * 출석체크
  
* **관리자전용 사이트 (추후 시간이 될때)**
  * 회원등록 및 변경
  * 수업등록 및 변경
  * 출석 조회 및 변경


# 현재까지 구현 사항
## RestAPI
|url|형식|매개변수|출력값|설명|
|--|--|--|--|--|
|/user|GET|id, password|로그인 여부|로그인 기능|
|/userinfo|GET|id|사용자 상세 정보|사용자에대한 정보를 받아옴|
|/usercourselist|GET|id|사용자 수업 수강 목록|수강중인 수업 조회|
|/coursetotalinformation|GET|courseid|수업 상세정보|수업 상세정보 조회(번호, 수업명, 강사, 시작시간, 진행시간, 강의실명, 진행요일)|
|/userattendancelist|GET|courseid, id|출석목록|해당 과목의 출석내역 조회|
|/notice|GET|X|전달사항|관리자프로그램의 전달사항 조회|
|/writenoticemessage|POST|id, message|전달사항|전달사항 등록|
|/userlist|GET|X|사용자|관리자프로그램의 사용자목록 조회|