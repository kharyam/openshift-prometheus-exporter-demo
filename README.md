# Prometheus Demo

1. Create config map for enabling service monitoring (tech preview).  Wait for prometheus pods to be running 

```
oc apply -f config.yml
watch oc -n openshift-user-workload-monitoring get pod
```

2. Deploy app that exposes metrics (privileged)

```
#oc apply -f prometheus-example-app.yml
oc project prometheus-demo
oc new-build --name=bios-exporter --strategy=docker --binary
oc start-build bios-exporter --from-dir=bios-exporter -wF
oc adm policy add-scc-to-user privileged -z default -n prometheus-demo
oc apply -f bios-exporter-app.yml
oc create serviceaccount grafana -n prometheus-demo
oc create clusterrolebinding grafana-cluster-monitoring-view --clusterrole=cluster-monitoring-view --serviceaccount=prometheus-demo:grafana
```

3. Create custom cluster role to allow access to metrics
```
oc apply -f custom-metrics-role.yml
```

4. Grant the role to any non cluster-admin users, e.g.
```
oc adm policy add-cluster-role-to-user monitor-crd-edit user1
``` 

5. Create a service monitor object to scrape the metrics exposed by the application
```
oc apply -f service-monitor.yml
```

6. Create alerts
```
oc apply -f app-alerting-rule.yml
```

7. Give view access to a user
```
oc policy add-role-to-user view username  -n prometheus-demo
```

8. Install grafana and grant permissions 
```
oc new-app grafana/grafana

```

9. Create grafana data sources and dashboard 
```
sed "s/SERVICE_SECRET/$(oc sa get-token grafana)/g" secret-openshift-ds.yml | oc apply -f -
oc apply -f dashboard-secret.yml 
oc apply -f dashboard-config-secret.yml 
``` 

10. Mount secrets
```
oc set volume dc/grafana --add --name=openshift-monitoring-grafana-datasource-volume --type=secret --secret-name=openshift-monitoring-grafana-datasource  --mount-path=/etc/grafana/provisioning/datasources
oc set volume dc/grafana --add --name=openshift-monitoring-grafana-dashboard-volume --type=secret --secret-name=openshift-monitoring-grafana-dashboard  --mount-path=/etc/grafana/provisioning/dashboards
oc rollout status dc/grafana
oc expose svc/grafana
```

11. Log in to grafana via the route as admin/admin
