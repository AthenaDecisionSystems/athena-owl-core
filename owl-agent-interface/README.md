# carbon-frontend Interface

### Prerequisites
- Install Node.js, npm and yarn
- Set the following environment variable: `NEXT_PUBLIC_BACKEND_BASE_API=http://localhost:8000/api/v1`

### Environment variable
```
cd owl-agent-interface
source ./setEnvironmentVariables.sh
```

### Build
```
cd owl-agent-interface
yarn 
```

### Run for dev
```
cd owl-agent-interface
yarn dev
```

### Create Docker image
```
cd owl-agent-interface
docker build -t owl-agent-interface .
```

### Add this to your docker-compose.yaml
```
athena-owl-agent-interface:
    hostname: athena-owl-agent-interface
    image: athena-owl-agent-interface:latest
    container_name: athena-owl-agent-interface
    ports:
      - 3001:3000
    environment:
      - NEXT_PUBLIC_BACKEND_BASE_API=http://localhost:8000/api/v1/
```