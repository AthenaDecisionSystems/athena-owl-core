from setuptools import setup, find_packages

setup(
    name="owl_agent_backend",
    version="0.1.0",
    description="The OWL Agent backend to support hybrid AI",
    author="Athena Decision Systems",
    packages=find_packages(include=["athena"]),
    install_requires=['uvicorn', 'fastapi', 'langchain-openai','langchain-anthropic','langchain_ibm','langchain_community',
'pydantic','python-multipart','python-dotenv','markdown','chromadb','pypdf'], 
)