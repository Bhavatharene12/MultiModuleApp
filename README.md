# 24MIS0505 – Multi-module App (MultiModule Student Management System)

Module 1 → Basic feature · Module 2 → Add feature · Connect → Link modules

| Version | Branch | What it contains | Look | Image | Deployment / Service | URL |
|---|---|---|---|---|---|---|
| **v1** | `v1` | **Module 1 only** – Add Student, Student List (no search, no dashboard) | Blue, top navbar | `bhavatharene12/multimoduleapp:v1` | `multimoduleapp-v1` / `multimoduleapp-service-v1` | http://localhost:30001 |
| **v2** | `v2` | **Module 2 only** – Search Student by ID / Name (no navigation, no dashboard) | Purple, centred search page | `bhavatharene12/multimoduleapp:v2` | `multimoduleapp-v2` / `multimoduleapp-service-v2` | http://localhost:30002 |
| **v3** | `main` | **Connected app** – Dashboard + Module 1 + Module 2, shared data | Green, sidebar dashboard | `bhavatharene12/multimoduleapp:v3` | `multimoduleapp-v3` / `multimoduleapp-service-v3` | http://localhost:30003 |

v2 searches a built-in sample list (5 students) because it has no Module 1. v3 starts with 3 sample students;
students added in Module 1 immediately appear in Module 2 search and on the dashboard (one shared list).

## Folder structure
```
MultiModuleApp/
├── v1/  app.py, templates/{base,add,students}.html, static/style.css
├── v2/  app.py, templates/{base,search}.html,        static/style.css
├── v3/  app.py, templates/{base,dashboard,add,students,search}.html, static/style.css
├── Dockerfile  Jenkinsfile  requirements.txt
├── deployment-v1/v2/v3.yaml   service-v1/v2/v3.yaml
├── git-setup.sh  build-images.sh / .bat  deploy-all.bat
└── README.md
```

## Prerequisites
VS Code, Python 3.10+, Git, Docker Desktop **with Kubernetes enabled**, Jenkins, GitHub and DockerHub (`bhavatharene12`) accounts.

## 1. Quick local check (optional)
```
pip install -r requirements.txt
cd v1 && python app.py        # http://localhost:5000  (same for v2, v3)
```

## 2. Git – three branches, own commits
Create an empty GitHub repo `MultiModuleApp`, then in **Git Bash** inside this folder:
```
bash git-setup.sh https://github.com/<your-username>/MultiModuleApp.git
```
Creates 3 commits each on `v1` → `v2` → `main` and pushes all three branches.

## 3. Docker – three different images
The Dockerfile uses `ARG VERSION` and copies only `v<VERSION>/`, so each image has different code and a different ID.
```
build-images.bat              (Windows)      or      bash build-images.sh
docker images
```
(If you build per branch, the Dockerfile default VERSION on each branch is already correct:
`docker build -t bhavatharene12/multimoduleapp:v1 .` on branch v1, `:v2` on v2, `:v3` on main.)

## 4. DockerHub
```
docker login
docker push bhavatharene12/multimoduleapp:v1
docker push bhavatharene12/multimoduleapp:v2
docker push bhavatharene12/multimoduleapp:v3
```

## 5. Jenkins (builds the correct version automatically)
1. Credentials → add *Username with password*, ID **`dockerhub-creds`** (DockerHub login/token).
2. New Item → **Multibranch Pipeline** → GitHub repo URL → Script Path `Jenkinsfile` → Scan.
3. Jenkins finds `v1`, `v2`, `main` and builds each. The Jenkinsfile maps branch → version (v1→1, v2→2, main→3) and runs:
   Git Checkout → Install requirements → Build Docker Image → Push Docker Image → Deploy Kubernetes.
Jenkins machine needs git, python, docker, kubectl (same PC as Docker Desktop is simplest).

## 6. Kubernetes
```
deploy-all.bat                (or kubectl apply -f deployment-vN.yaml -f service-vN.yaml for N=1,2,3)
kubectl get deployment
kubectl get all
```
Open http://localhost:30001 , :30002 , :30003.

## 7. Screenshot checklist
1 GitHub branches · 2 GitHub commits · 3 v1 UI (add a few students, show list) · 4 v2 UI (search `24MIS0505` / `Priya`) ·
5 v3 UI (dashboard; also add a student then search it) · 6 Jenkins successful build · 7 `docker images` · 8 DockerHub tags ·
9 `kubectl get deployment` · 10 `kubectl get all` · 11–13 localhost:30001 / 30002 / 30003.

## Troubleshooting
* `ImagePullBackOff` → push the image first / `docker login`.
* Port not opening → `kubectl get svc`; check Kubernetes is enabled in Docker Desktop.
* Data is in memory – resets when a pod restarts.
* After code changes: rebuild → push → `kubectl rollout restart deployment/multimoduleapp-vN`.
