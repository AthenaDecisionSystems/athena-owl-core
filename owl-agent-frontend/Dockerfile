# Step 1: build the application
FROM node:14 AS build

ARG AGENT_NAME="Miniloan Agent"
ARG BACKEND_URL="http://localhost:8000/api/v1/"
ARG ASSISTANT_ID="ibu_assistant"
ARG AGENT_ID="ibu_agent"
ARG DEFAULT_PROMPT='ibu_loan_prompt'
ARG DEMO_TEXT "One of our client Robert Smith wants a loan for $500,000 for a duration of 60 months do we approve it?"

ENV REACT_APP_AGENT_NAME=${AGENT_NAME}
ENV REACT_APP_BACKEND_URL=${BACKEND_URL}
ENV REACT_APP_ASSISTANT_ID=${ASSISTANT_ID}
ENV REACT_APP_AGENT_ID=${AGENT_ID}
ENV REACT_APP_DEFAULT_PROMPT=${DEFAULT_PROMPT}
ENV REACT_APP_DEMO_TEXT = ${DEMO_TEXT}

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Step 2: Serve it with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]