# Owl Backend to support multiple demo

For getting multiple demos in the same backend we can add the concept of apps.

In the docker image the owl_backend can be organized as

/owl-backend/athena   -> backend source code
/owl-backend/apps/base/config   -> folder with the current config folder content from src/athena/config
/owl-backend/apps/ibu-insurance/config  -> folder for the specific configuration of the agents, tools, prompt
/owl-backend/apps/ibu-insurance/src   -> specific python code for tools and integration 
/owl-backend/apps/ibm-loan-demo/config
/owl-backend/apps/ibm-loan-demo/src


When the owl-backend starts it can list the content of /owl-backend/apps folders to see the apps present and merge the agents, tools, and prompts definitions.
For the code to be executable we need to set the PYTHONPATH to the demo code src.

The code and config for a demos still come from a dedicated repostiory. 
To run the demo locally we contiue to mount code and config inside the docker container.

Once deployed on k8s we can copy the content of the demo to /owl-backend/apps/ via kubectl cp

