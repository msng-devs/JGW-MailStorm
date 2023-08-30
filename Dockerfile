FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

RUN mkdir ./data
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo '#!/bin/sh\npython /app/cmd.py "$@"' > /usr/local/bin/mailstorm
RUN chmod +x /usr/local/bin/mailstorm

ENTRYPOINT ["python3","main.py"]