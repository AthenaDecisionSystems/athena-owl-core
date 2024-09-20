from setuptools import setup, find_packages

setup(
    name="athena-owl-agent",
    version="0.1.0",
    description="The backend to support hybrid AI",
    author="Jerome Boyer",
    packages=find_packages(include=["athena-owl-agent"]),
    install_requires=[ 'langchain-openai','langchain_community',
'pydantic','python-dotenv']
)
