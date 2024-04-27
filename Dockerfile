from python:latest
WORKDIR /app
COPY . /app
RUN pip install poetry
RUN poetry install
ENTRYPOINT ["poetry", "run", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0"]
