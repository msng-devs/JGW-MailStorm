# Mail Storm 
## 자람 그룹웨어 메일 발송

자람 그룹웨어에 사용되는 메일 발송 서비스입니다.

### 소개

해당 서비스는 ZMQ를 활용한 메일 발송 서비스입니다. 

Pipeline 패턴을 사용하여 구현되어있으며, 백엔드 서비스에 PUSH 소켓을 구성하여 연동합니다.

Jinja2 기반 템플릿 엔진을 사용하여 손쉽게 메일 템플릿을 구성할 수 있습니다.

### 사용법 - 서비스 구성

해당 서비스는 Docker를 사용하여 구성되어있습니다.

1. 해당 repository를 clone합니다.
```bash
git clone https://github.com/msng-devs/JGW-MailStorm
```
2. 디렉토리 최상단에 .env 파일을 생성하고 아래 내용을 추가합니다.
```bash
COLLECTOR_PORT= COLLECTOR가 사용할 포트입니다. WORKER 의 처리 결과를 수신합니다.
WORKER_PORT= WORKER가 사용할 포트입니다. 해당 포트로 메시지를 수신합니다.
WORKER_POOL_SIZE= WORKER의 갯수를 지정합니다.
SMTP_HOST= SMTP 서버의 호스트 주소입니다.
SMTP_PORT= SMTP 서버의 포트입니다.
SMTP_USER= SMTP 서버의 사용자 이름입니다.
SMTP_PASSWORD= SMTP 서버의 비밀번호입니다.
SMTP_FROM= SMTP 서버의 발신자 주소입니다.
```

3. Dockerfile을 빌드합니다.
```bash
docker build -t your-image-name .
```

4.생성된 이미지를 사용하여 컨테이너를 실행합니다.
```bash
docker run -d \
  --name your-container-name \
  -v /path/to/data:/app/data \
  -p smtp-port:smtp-port \
  your-image-name
```
*smtp-port 는 SMTP 서버의 포트입니다. 해당 포트를 외부에 노출시켜야 메일 발송이 가능합니다.*

*필요할 경우 WORKER의 포트를 노출해야합니다. 해당 WORKER의 포트로 메시지를 전송해야합니다.*

*/app/data 디렉토리에 템플릿 파일 및 database 파일이 생성됩니다.*

### 사용법 - 메일 발송

서비스를 사용하기 위해서는, 소개 항목에서 언급한 것 처럼 PUSH 소켓을 구성해야합니다.

해당 문서에서는 Python을 사용한 예시를 제공합니다. 그 외 언어는 [ZMQ 공식 문서](https://zeromq.org/get-started/)를 참고하세요. 

#### Python 예시
```python
import json
import zmq


def push_socket():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://host:port")
    
    message = "{some message}"
    request = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
    zmq_socket.send_json(request)
```
기본적으로 해당 서비스는 TCP 프로토콜을 사용합니다. 따라서 PUSH 소켓을 구성할 때 TCP 프로토콜을 사용하도록 구성해주세요.

또한 Json 형태로 메시지를 받기 때문에 발송할 내용을 변환하여 전송해야합니다.

*한글의 경우 ensure_ascii=False 옵션을 사용하지 않으면 메시지 내용이 정상적으로 전달되지 않을 수 있습니다. 반드시 해당 옵션을 사용하여 json.dumps 함수를 사용하세요.*

해당 서비스에서 사용하는 message 형태는 아래와 같습니다.

#### Message
```json
{
  "to" : "발송 대상",
  "subject" : "이메일 제목",
  "template" : "사용할 템플릿 이름",
  "arg" : {
    "사용할 인자 명" : "해당하는 값"
  },
  "who" : "해당 시스템을 사용하는 microservice의 이름"
}
```
반드시 위 형태를 지켜서 메시지를 전송해야합니다.



#### 기본 템플릿 (plain_text)
기본적으로 해당 시스템에서는 사용자 정의 템플릿 외에 plain_text 템플릿을 제공합니다.
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject }}</title>
</head>
<body>
    <p>{{ content }}</p>
</body>
</html>
```
| 인자명  | 설명                    |
| ------- | ----------------------- |
| content | 메일의 메인 내용입니다. |
| subject | 메일의 제목입니다.      |


해당 템플릿을 사용한 예시는 아래와 같습니다.
```json
{
  "to" : "test@test.test",
  "subject" : "[자람 그룹웨어] 회원 가입을 축하합니다!",
  "template" : "plain_text",
  "arg" : {
    "content" : "축하합니다! 자람 그룹웨어에 오신걸 환영합니다!",
    "subject" : "회원 가입을 축하합니다!" 
  },
  "who" : "mms"
}
```

#### 사용자 정의 템플릿

Jinja2를 사용하여 사용자 정의 템플릿을 구성할 수 있습니다.

하지만 해당 서비스에서 Jinja로 작성된 템플릿을 사용하기 위해서는 아래 형식을 반드시 지켜야합니다.
```html
<!--subject;content-->
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject }}</title>
</head>
<body>
    <p>{{ content }}</p>
</body>
</html>
```
위 예시 처럼 반드시 최상단 첫번째 라인에 해당 템플릿에서 사용하는 인자를 선언해야합니다.

param1;param2;param3... 형태로 선언하며, 인자의 갯수는 제한이 없습니다. 단 구분자로 ; 를 사용해야합니다.

해당 인자가 누락되어있을 경우 정상적으로 메일이 발송되지 않거나, 템플릿 초기화 과정에서 반영이 되지 않을 수 있습니다.

작성된 템플릿은 '/data/template' 경로에 저장해야합니다.

*만약 해당 서비스가 동작중일 때 템플릿을 추가하면 반영되지 않습니다. 아래 Controller 항목을 참고하여 갱신해주어야합니다.*

### 사용법 - Mail Storm Controller

Mail Storm Controller는 해당 Mail Storm을 관리할 수 있는 간단한 툴입니다.

실행 방법은 아래와 같습니다.
1. 컨테이너 접속
```bash
docker exec -it your_container_name /bin/bash
```
해당 서비스가 실행중인 컨테이너에 접근합니다.

2. 컨트롤러 실행
```bash
./mailstorm
```
이후 아래에서 제공하는 명령어를 사용하여 간단한 기능들을 사용할 수 있습니다.

#### 명령어

#### help or ? : 도움말
```bash
help
```
도움말을 확인합니다.

#### exit : 종료
```bash
exit
```

##### show : 템플릿 목록 확인
```bash
show 10
```
템플릿 목록을 확인합니다. 인자로 템플릿 목록을 몇개까지 보여줄지 지정할 수 있습니다. (기본값 10개)

##### history : 발송 이력 확인
```bash
history 10
```
발송 이력을 확인합니다. 인자로 발송 이력을 몇개까지 보여줄지 지정할 수 있습니다. (기본값 10개)

##### refresh : 템플릿 갱신
```bash
refresh
```
템플릿을 갱신합니다. 템플릿을 새로 추가했거나 템플릿을 제거했을 경우 해당 명령어를 실행하여 목록을 갱신하여야합니다.

*단 템플릿 수정은 갱신을 시킬 필요가 없습니다*
