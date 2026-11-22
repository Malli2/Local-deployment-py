FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080 APP_NAME="MTS Deployment Platform" APP_ENV=kubernetes
WORKDIR /opt/mts-demo
COPY app/ ./app/
RUN useradd --create-home --uid 10001 appuser
USER 10001
EXPOSE 8080
CMD ["python", "app/app.py"]
