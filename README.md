# Aplikasi shortlink sederhana gabut buat belajar DevOps

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
- [x] Jenkins
- [x] Build & push ke registry
- [x] k8s (k3s)
- [ ] Full pipeline
- [ ] GitOps
- [ ] ArgoCD
- [ ] Monitoring (Grafana & Prometheus)
