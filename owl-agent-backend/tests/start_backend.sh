export CONFIG_FILE=./tests/it/config/config.yaml
export OWL_CLIENTS=[http://localhost:3000]
export PYTHONPATH=./src
cd ..
uvicorn athena.main:app --host 0.0.0.0 --port 8002 --reload 