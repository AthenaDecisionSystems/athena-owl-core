# carbon-frontend Interface

### Prerequisites
- Install Node.js, npm and yarn
- Set the following environment variable: `NEXT_PUBLIC_BACKEND_BASE_API=http://localhost:8000/api/v1/`

### Environment variable
```
cd owl-agent-interface
source ./setEnvironmentVariables.sh
```

_Note: the is another environment variable that is processed by the frontend. The name is NEXT_PUBLIC_DEMO_TEXT. Its content is automatically entered in the chat text area when you enter demo. See below for an example in IBU Insurance Demo_

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
      - NEXT_PUBLIC_DEMO_TEXT="Hi IBU, I am on the phone with one of my very important customer. Her name is Sonya Smith. She has a problem with her claim 2 for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. Sonya finds this very disappointing. What would be the next best action?"

```