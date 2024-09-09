FROM python:3.10.14-bookworm
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r src/requirements.txt
EXPOSE 8000

CMD [ "fastapi", "run", "src/main.py"]