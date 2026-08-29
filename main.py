import os

import uvicorn


def run() -> None:
    uvicorn.run(
        "app:app",
        app_dir="app",
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT", "8000")),
        reload=os.getenv("APP_RELOAD", "true").lower() == "true",
    )


if __name__ == "__main__":
    run()
