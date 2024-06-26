import requests
import unittest

IBU_BASE_URL="http://localhost:8000/api/v1"
class TestMistralToolOllama(unittest.TestCase):
    
    
    def test_call_using_web_search(self):
        print("\n--> Call Mistral on Ollama with information its was not train on\n")
        data='{ "locale": "en",\
            "query": "what is the company Athena Decision Systems.",\
            "type": "chat",\
            "assistant_id":"mistral_tool_assistant",  \
            "user_id" : "it_tester", \
            "thread_id": "1" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
        assert rep
        
        
if __name__ == "__main__":
    unittest.main()