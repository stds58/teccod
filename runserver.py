from pathlib import Path

import uvicorn

CERTS_FOLDER = Path(__file__).parent.joinpath("certs")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        #host="localhost",
        port=8000,
        reload=True,
    )
