.PHONY: create_ns
# Setting global variables
DEV_NS=owl

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