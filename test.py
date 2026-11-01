from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    
    print("hello")
    return {"message": "Hello"}