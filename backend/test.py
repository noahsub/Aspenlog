import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import NBCC_Data_Extraction

app = FastAPI()


@app.get("/")
def read_root():
    return {"SEEDA-UOFT Backend": "Running"}

@app.get("/table_c2")
def table_c2():
    return HTMLResponse(content=NBCC_Data_Extraction.table_c2_extraction().to_html(), status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
