FROM python:3.10

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#run ->docker執行的，--no-cache-dir->不須快取、--upgrade更新 -r遞回去安裝
COPY ./app /code/app
#將本機的app複製到containe的app
CMD [ "fastapi","run","app/main.py","--port","80" ]
#fastapi run app/main.py --port 80 (cmd會打的指令)