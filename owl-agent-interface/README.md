# carbon-frontend Interface

### Prerequisites
- Install Node.js, npm and yarn
- Set the following environment variable: `NEXT_PUBLIC_BACKEND_BASE_API=http://localhost:8000/api/v1/`

_Depending on your owl-backend server, the URL or port could be different._

### Environment variables
```
cd owl-agent-interface
source ./setEnvironmentVariables.sh
```

_Note: there are other environment variables that are processed by the frontend._  
**NEXT_PUBLIC_DEMO_TEXT**_'s content is automatically entered in the chat text area when you enter the string `demo`. See below for an example in IBU Insurance Demo._  
**NEXT_PUBLIC_COLLECTION_NAME** _is the collection name in the vector store associated with your demo. This name is also declared in the config.yaml file. If not provided, `owl_default` is the default value for the frontend._  
**NEXT_PUBLIC_SHOW_SETTINGS_AND_DOCUMENTS** _indicates with yes or no or true or false whether the accordion with Settings and Documents is displayed or not._  

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
      - NEXT_PUBLIC_COLLECTION_NAME=ibu_insurance
      - NEXT_PUBLIC_DEMO_TEXT="Hi IBU, I received an email from my customer Sonya Smith. She has a problem with her claim number 2 for their water damage. She told me that the carpet is very expensive. She is surprised that her insurance policy does not cover damage to her valuables. Sonya finds this very disappointing. What should I answer?"

```