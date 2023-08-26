import uvicorn
from fastapi import FastAPI
from routers import user,login,testReq

app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)
app.include_router(testReq.router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
    # uvicorn.run(app)