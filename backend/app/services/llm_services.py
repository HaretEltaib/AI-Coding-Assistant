from llama_index.llms.ollama import Ollama

def chat(prompt: str):
    llm_model = Ollama(model="llama3.2:1b")
    response = llm_model.complete(prompt)
    return response.text
def greet(name="gust") :
    return
    
    