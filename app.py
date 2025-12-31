import os
from fastapi import FastAPI, HTTPException
from pyvesync.vesync import VeSync

app = FastAPI(title="VeSync Filter Reset API")

EMAIL = os.getenv("VESYNC_EMAIL")
PASSWORD = os.getenv("VESYNC_PASSWORD")
TIMEZONE = os.getenv("VESYNC_TIMEZONE", "America/New_York")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/reset-filters")
async def reset_filters():
    if not EMAIL or not PASSWORD:
        raise HTTPException(status_code=500, detail="Missing VESYNC_EMAIL or VESYNC_PASSWORD")

    results = []

    async with VeSync(
        username=EMAIL,
        password=PASSWORD,
        country_code="US",
        time_zone=TIMEZONE,
        redact=True
    ) as manager:
        if not await manager.login():
            raise HTTPException(status_code=401, detail="VeSync login failed")

        await manager.update()

        for fan in manager.devices.air_purifiers:
            try:
                await fan.reset_filter()
                results.append({"device": fan.device_name, "reset": True})
            except Exception as e:
                results.append({"device": fan.device_name, "reset": False, "error": str(e)})

    return {"status": "success", "results": results}
