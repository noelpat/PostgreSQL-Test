# Please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

ADD app.py .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

#RUN useradd -u 1001 appuser && chown -R appuser /app
#USER 1001

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
