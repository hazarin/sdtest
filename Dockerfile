FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x /code/start.sh
RUN python manage.py migrate
RUN python manage.py loaddata schedule.json
RUN python manage.py load_participants participants.jsonl
EXPOSE 8000:80
CMD ["sh", "start.sh"]