# Prometheus Demo

This project demonstrates the deployment of a custom promethetheus exporter in OpenShift 4.x

![Grafana Dashboard](images/grafana.png)


## Deploying the Demo

1. Create config map for enabling service monitoring (tech preview).  Wait for prometheus pods to be running 

```
oc apply -f config.yml
oc rollout status sts/prometheus-user-workload -n openshift-user-workload-monitoring -w
```

2. Deploy app that exposes metrics (privileged)

```
oc new-project prometheus-demo
oc apply -f build.yml -n prometheus-demo
oc start-build bios-exporter --from-dir=bios-exporter -wF -n prometheus-demo
oc adm policy add-scc-to-user privileged -z default -n prometheus-demo
oc apply -f bios-exporter-app.yml -n prometheus-demo
oc create serviceaccount grafana -n prometheus-demo
oc create clusterrolebinding grafana-cluster-monitoring-view --clusterrole=cluster-monitoring-view --serviceaccount=prometheus-demo:grafana
```


3. Install grafana, data sources and dashboard 
```
sed "s/SERVICE_SECRET/$(oc sa get-token grafana)/g" grafana.yml | oc apply -f - -n prometheus-demo
oc rollout status deployment/grafana -n prometheus-demo
oc create route edge grafana --service=grafana -n prometheus-demo
```

4. Log in to grafana via the route as admin/admin and navigate to the **BIOS Information** dashboard
```
oc get routes
```

## Optional Steps (Grant Access)

1. Grant the custom cluster role for metrics to any non cluster-admin users, e.g.
```
oc adm policy add-cluster-role-to-user monitor-crd-edit username 
``` 

2. Give view access to the project to a user
```
oc policy add-role-to-user view username  -n prometheus-demo
```
