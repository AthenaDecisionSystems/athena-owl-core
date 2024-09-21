.PHONY: create_ns e2e_owl_backend
# Setting global variables
DEV_NS ?= ibu
OWL_BACKEND ?= owl-backend
OWL_FRONTEND ?= owl-frontend
# -------------------------------------------------------
# Entry points
# -------------------------------------------------------
prepare: create_ns create_secret_from_env

all: prepare


ensure_ns = \
	@kubectl get ns $1 >/dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
			kubectl create ns $1; \
	else \
			echo "$1 exists";\
	fi

create_ns:
	$(call ensure_ns, $(DEV_NC))

create_secret_from_env:
	@kubectl create  secret generic env  --from-env-file=../local/.env -n $(DEV_NS)

deploy_owl_backend:
	@helm install $(OWL_BACKEND) $(OWL_BACKEND) -n $(DEV_NS)

upgrade_owl_backend:
	@helm upgrade $(OWL_BACKEND) $(OWL_BACKEND)  -n $(DEV_NS)

deploy_decision_svc:
	@helm install -name decision-svc decision-svc -n $(DEV_NS)

deploy_owl_frontend:
	@helm install -name $(OWL_FRONTEND) $(OWL_FRONTEND) -n $(DEV_NS)

upgrade_owl_frontend:
	@helm upgrade $(OWL_FRONTEND) $(OWL_FRONTEND)  -n $(DEV_NS)

clean:
	@helm delete $(OWL_FRONTEND) 
	@helm delete $(OWL_BACKEND)
	@helm delete decision-svc 

set_k8s_context:
	@kubectl config  --kubeconfig=/home/jbcodeforce/.kube/config  use-context athena-demo

	
get_owl_backend_address:
	@echo "Fetching external address for $(OWL_BACKEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$$ADDRESS" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$$ADDRESS" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(OWL_BACKEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:8000/api/v1/version; \
	fi

get_owl_front_address:
	@echo "Fetching external address for $(OWL_FRONTEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$$ADDRESS" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$$ADDRESS" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:3000/; \
	fi