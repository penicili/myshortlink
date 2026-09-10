# API shortlink buat belajar DevOps

endpoints:

1. POST / Request body long link; Response short link
2. GET /{shortlink} Redirect ke long link
3. DELETE /{shortlink} del record shortlink
4. GET / health check

---

rencana:

- [x] Base app
- [x] Github
- [x] Docker
- [x] Jenkins (pre argo)
- [x] Build & push ke registry
- [x] k8s (kind)
- [x] Full pipeline
- [x] ArgoCD
- [x] Github Actions
- [x] GitOps
- [x] Backstage Component (catalog-info)
- [ ] Observability


---
### Pipeline
1. Jenkins Pipeline (udh gadipake): Test and build image, lalu push ke docker hub= (run on agent jenkins)
2. Github Actions Pipeline: Build image, push ke docker hub (run on Github actions runner). trigger update ArgoCD (run onself-hosted runner)