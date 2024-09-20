.PHONY: create_ns
# Setting global variables
DEV_NS=ibu

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
	@helm install owl-backend owl-backend -n $(DEV_NS)

upgrade_owl_backend:
	@helm upgrade owl-backend owl-backend -n $(DEV_NS)

deploy_decision_svc:
	@helm install -name decision-svc decision-svc -n $(DEV_NS)

deploy_owl_frontend:
	@helm install -name owl-frontend owl-frontend -n $(DEV_NS)

clean:
	@helm delete owl-frontend 
	@helm delete owl-backend 
	@helm delete decision-svc 