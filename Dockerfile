# One Dockerfile for all versions. Jenkins passes --build-arg VERSION=<n> automatically from the branch.
# The default VERSION differs per Git branch (v1 branch -> 1, v2 branch -> 2, main -> 3),
# so plain "docker build -t bhavatharene12/multimoduleapp:vN ." gives a different image per version.
FROM python:3.12-slim

ARG VERSION=3
LABEL maintainer="24MIS0505" \
      project="MultiModule Student Management System" \
      app.version="v${VERSION}"

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY this version's code (v1, v2 or v3) -> different content = different image ID
COPY v${VERSION}/ /app/

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
