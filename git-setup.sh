#!/bin/bash
# Creates the Git history: v1 branch -> v2 branch -> main (v3), each with its own commits.
# Run in Git Bash (Windows) or any bash shell, from inside the MultiModuleApp folder.
# Usage:  bash git-setup.sh https://github.com/<your-username>/MultiModuleApp.git
set -e
REMOTE="$1"

git init
git config user.name  >/dev/null || git config user.name  "24MIS0505"
git config user.email >/dev/null || git config user.email "24mis0505@vitstudent.ac.in"

# ---------------- VERSION 1 (branch v1) ----------------
git checkout -b v1
sed -i 's/^ARG VERSION=.*/ARG VERSION=1/' Dockerfile
git add .gitignore .dockerignore requirements.txt Dockerfile
git commit -m "v1: project setup - requirements, Dockerfile (VERSION=1)"
git add v1
git commit -m "v1: Module 1 only - Add Student, Student List (in-memory)"
git add Jenkinsfile deployment-v1.yaml service-v1.yaml README.md git-setup.sh build-images.sh build-images.bat deploy-all.bat
git commit -m "v1: Jenkinsfile + Kubernetes deployment/service (port 30001)"

# ---------------- VERSION 2 (branch v2) ----------------
git checkout -b v2
sed -i 's/^ARG VERSION=.*/ARG VERSION=2/' Dockerfile
git add Dockerfile
git commit -m "v2: Dockerfile builds version 2"
git add v2
git commit -m "v2: Module 2 only - Search Student by ID / Name (simple search UI)"
git add deployment-v2.yaml service-v2.yaml
git commit -m "v2: Kubernetes deployment/service (port 30002)"

# ---------------- VERSION 3 (branch main) ----------------
git checkout -b main
sed -i 's/^ARG VERSION=.*/ARG VERSION=3/' Dockerfile
git add Dockerfile
git commit -m "v3: Dockerfile builds version 3"
git add v3
git commit -m "v3: Connect Module 1 + Module 2 - dashboard, navigation, shared data"
git add deployment-v3.yaml service-v3.yaml
git commit -m "v3: Kubernetes deployment/service (port 30003)"

git log --oneline --all --graph

if [ -n "$REMOTE" ]; then
  git remote add origin "$REMOTE"
  git push -u origin v1 v2 main
  echo "Pushed v1, v2 and main to $REMOTE"
else
  echo "Local history created. Add a remote and run: git push -u origin v1 v2 main"
fi
