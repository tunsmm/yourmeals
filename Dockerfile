FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN pip install spacy
RUN python -m spacy download ru_core_news_lg
RUN pip install -r requirements.txt
WORKDIR /app
ADD . /app
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
