FROM python:3.9

RUN mkdir -p /docker/app/bot_game_word/
WORKDIR /docker/app/bot_game_word/

COPY . /docker/app/bot_game_word/
RUN pip install -r requirements.txt

CMD ["python","main.py"]