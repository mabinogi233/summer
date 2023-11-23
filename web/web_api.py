from fastapi import FastAPI
from pydantic import BaseModel

from summer.web.webcontainer import web_content
from summer.core.scheduler.scheduler import start

app = FastAPI()

class Item(BaseModel):
    data: dict

@app.post("/{path:path}")
async def handle_request(path: str, item: Item):
    _path = path.strip("/")
    data = item.data
    output = {"service error": "service not found"}
    for web_url in web_content.get_names():
        if web_url == _path:
            output = web_content.get(web_url).run(data)
            break
    return output


if __name__ == "__main__":
    start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=23045)