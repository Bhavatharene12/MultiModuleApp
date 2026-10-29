@echo off
REM Builds all three DIFFERENT images (v1, v2, v3) - Windows CMD / PowerShell
for %%n in (1 2 3) do docker build --build-arg VERSION=%%n -t bhavatharene12/multimoduleapp:v%%n .
docker images bhavatharene12/multimoduleapp
