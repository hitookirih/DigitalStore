import uvicorn
from fastapi import FastAPI

from api import router as api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main_app", host="0.0.0.0", port=8000, reload=True)
