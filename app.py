from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from WaLSAtools import WaLSAtools
import numpy as np
import tempfile

app = FastAPI(title="WaLSAtools API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_analysis(
    signal: UploadFile = File(...),
    time: UploadFile = File(...),
    method: str = Form("fft")
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as sig_temp, tempfile.NamedTemporaryFile(delete=False) as time_temp:
            sig_temp.write(await signal.read())
            time_temp.write(await time.read())
            sig_temp.flush()
            time_temp.flush()

            signal_array = np.load(sig_temp.name)
            time_array = np.load(time_temp.name)

        power, freqs, sig, _ = WaLSAtools(signal=signal_array, time=time_array, method=method)

        return JSONResponse({
            "frequencies": freqs.tolist(),
            "power": power.tolist(),
            "significance": sig.tolist()
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
