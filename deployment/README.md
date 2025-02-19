# Kubernetes Deployment for owl-backend and front-end

This documents describes the steps to deploy the owl-backend.

## A Kubernetes Playground

If you know nothing about Kubernetes, maybe start with [this official tutorial](https://kubernetes.io/docs/tutorials/), RedHat has also very [good content starting with](https://developers.redhat.com/products/openshift/overview). Also for ODM experts, it is mandatory to read [this git repo: Deploying IBM Operational Decision Manager on a Certified Kubernetes Cluster.](https://github.com/DecisionsDev/odm-docker-kubernetes)

We recommend using a local kubernetes with Minikube (See [installation guide](https://kubernetes.io/docs/tasks/tools/install-minikube)) or with [KinD](https://kind.sigs.k8s.io/docs/user/quick-start).

### Tools needed

The following CLI are needed:

* helm [See installation instructions.](https://helm.sh/docs/intro/quickstart/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* The `.env` file with the different environment variables used in the OWL Backend with API Key secrets.
* make CLI

### Access to Scaleway

To access Scaleway, there is a kubernetes cluster already created by a system administrator. Be sure to get the security tokens and the access username within the file named: 
`athena-demo_ibu_kubeconfig`, which is a kubeconfig specification manifest used to access the athena-demo cluster with write access on `ibu` namespace. Normally this file can be saved under `$HOME/.kube` folder. (If you have an existing `.kube/config` file to define existing Kubernetes contexts, then you may want to merge the  `athena-demo_ibu_kubeconfig` content into this `.kube/config` file, and then set the current context to `athena-demo`). 

Use this command to specify the kubectl context to use, so that all commands done with kubectl will go to the Scaleway cluster.

```sh
export KUBECONFIG=~/.kube/athena-demo_ibu_kubeconfig
```

* Verify you can access the Scaleway cluster:

* List the nodes within Kubernetes

```sh
$ kubectl get nodes 
NAME                                             STATUS   ROLES    AGE     VERSION
scw-athena-demo-infra-4c7f37b95e7a40d7b78375fb   Ready    <none>   4h55m   v1.30.2
scw-athena-demo-runners-a1fb1bcfe50647eabf642c   Ready    <none>   122m    v1.30.2
```

* Verify the namespaces

```sh
kubectl get  ns
```

The current namespace for the demonstration is `ibu`

## Owl-backend deployment

To deploy the secrets for the LLM API Keys, get your .env file and do

```sh
make create_secret_from_env
# 
kubectl get secret owl-dotenv -o jsonpath='{.data.\.env}'  | base64 --decode
```

* Use make to deploy the backend

```sh
make deploy_owl_backend
# Or if already deployed
make upgrade_owl_backend
```

* Verify the pods

```sh
kubectl get pods
```

* Get the IP address

```sh
kubectl get --namespace ibu svc -w owl-backend
```