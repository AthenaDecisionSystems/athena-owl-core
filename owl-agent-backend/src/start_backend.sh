export CONFIG_FILE=./dev-config.yaml
export OWL_CLIENTS=[http://localhost:3000]

uvicorn athena.main:app --host 0.0.0.0 --port 8000 --reload 