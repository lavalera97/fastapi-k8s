<h3 align="center">FastAPI in k8s</h3>

### Description

This repo contains simple FastAPI project with one route ```/health```.

It's dockerized and contains basic manifests for k8s:

* *Deployment* - runs multiple replicas of application and automatically replaces any instances that fail or become 
  unresponsive.

* *Service* - defines a logical set of pods and a policy by which to access them. As Pods have different internal IP 
  address that can change, we use service to get a stable IP address that lasts for the life of itself.
  
* *Ingress* - exposes HTTP and HTTPS routes from outside the cluster to services within the cluster.It allows us 
  to consolidate our routing rules into a single resource. 
  
> As we don't use multiple services, our ingress contains only one host and http path.

### Instructions 

#### Activate Ingress

We have to activate ingress as it's included in manifests.

Using minikube you can simply activate it with command below.

```
minikube addons enable ingress
```

![ingress install](https://www.dropbox.com/s/zut43cpa3r5iy1i/ingress_install.PNG?dl=0)

Other methods are explained in 
<strong> [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/) </strong>

#### Apply k8s manifests

```
kubectl apply -f k8s/
```

![](https://www.dropbox.com/s/xmt827wth1yznkj/k8s%20apply.png?dl=0)

