# Mail Storm 
## 자람 그룹웨어 메일 발송
*설명 추가 예정*

### Client
```json
{
  "to" : "발송 대상",
  "subject" : "이메일 제목",
  "template" : "사용할 템플릿 이름",
  "arg" : {
    //템플릿에 사용할 인자들
    "foo" : "boo" 
  },
  "who" : "해당 시스템을 사용하는 microservice의 이름"
}
```

#### 기본 템플릿 (plain_text)
기본적으로 해당 시스템에서는 사용자 정의 템플릿 외에 plain_text 템플릿을 제공합니다.
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