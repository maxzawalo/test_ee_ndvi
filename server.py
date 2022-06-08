import time
from img_from_geojson import *
import uvicorn
from fastapi import File, UploadFile, FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/ndvi_from_geojson")
async def ndvi_from_geojson(file: UploadFile = File(...)):
    ts = time.time_ns()
    try:
        contents = await file.read()
        with open(get_json_path(ts), 'wb') as f:
            f.write(contents)
        img_from_geojson(ts)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    return FileResponse(get_image_path(ts))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)