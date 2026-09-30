# ---- build stage ----
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- runtime stage ----
FROM python:3.12-slim
WORKDIR /app
COPY --from=build /install /usr/local
COPY app.py .
# arbitrary non-root UID: also compatible with OpenShift restricted SCC
USER 1001
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "2", "app:app"]