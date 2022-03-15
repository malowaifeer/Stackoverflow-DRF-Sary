1. Test Django
```
python manage.py test
```

2. Build Docker Container
```
docker build -f Dockerfile  \
    -t registry.digitalocean.com/stackoverflow-k8s/stackoverflow-drf:latest \
    -t registry.digitalocean.com/stackoverflow-k8s/stackoverflow-drf:v1 \
    .
```

3. Push Docker Container to Digital Ocean Registry
```
docker push registry.digitalocean.com/stackoverflow-k8s/stackoverflow-drf --all--tags
```

4. Update Secrets
```
kubectl delete secret stackoverflow-drf-prod-env
kubectl create secret generic stackoverflow-drf-prod-env --from-env-file=./.env.prod
```

5. Update Deployment
```
kubectl apply -f k8s/apps/stackoverflow-drf.yaml
```

6. Wait for Rollout to Finish
```
kubectl rollout status deployment/stackoverflow-drf-deployment
```

7. Migrate Database
```
export SINGLE_POD_NAME=$(kubectl get pod -l app=stackoverflow-drf-deployment -o jsonpath="{.items[0].metadata.name}")
```

Run Migration
```
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```