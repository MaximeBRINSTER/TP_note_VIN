from fastapi import FastAPI
import predict
import model

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "This API isn't finished ... and maybe will never be finished"}

app.include_router(predict.router)

app.include_router(model.router)