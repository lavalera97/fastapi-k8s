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

<div style="text-align: center">
<img src="https://user-images.githubusercontent.com/80529021/177394397-8a422776-edbd-422e-94b2-93a45f17f3d8.PNG" alt="ingress_install"  width="95%"/>
</div>

Other methods are explained in 
<strong> [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/) </strong>

#### Apply k8s manifests

```
kubectl apply -f k8s/
```

<div style="text-align: center">
<img src="https://user-images.githubusercontent.com/80529021/177394747-60922217-1e4e-407c-838d-1c705669d10b.png" alt="k8s apply"  width="95%"/>
</div>

#### Allow local access to host "service" in ingress

As we are using "service" as dns name, we have to add it to ```etc/hosts``` file with ip mentioned in ingress 

```
kubectl get ing
```

![ingress-webapp](https://user-images.githubusercontent.com/80529021/177397596-233ccadc-7a8e-4042-ba8b-3c56238f907d.PNG)

>  Using minikube
>```
>minikube ip
>```

Then open ```etc/hosts``` as administrator and add ```<YourIP> service``` at the end of the file

> **Windows**: c:\windows\system32\drivers\etc\hosts
> 
> **Linux, Unix, BSD** — /etc/hosts
> 
> **MacOS** — /private/etc/hosts

![hosts](https://user-images.githubusercontent.com/80529021/177399509-fc2e3d2f-3f3f-47df-926f-0d96dc805882.PNG)

#### Check if everything works

* **Send request**
```
curl --location --request GET 'http://service/health'
```

* **Visit site**

> http://service/health


* Make request from swagger

> http://service/docs

![webapp-swagger](https://user-images.githubusercontent.com/80529021/177400881-ce95cb8d-0b44-4219-8613-34cc3e9c9339.PNG)
