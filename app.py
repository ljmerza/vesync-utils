import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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

    async with VeSync(
        username=EMAIL,
        password=PASSWORD,
        country_code="US",
        time_zone=TIMEZONE,
        redact=True,
    ) as manager:
        if not await manager.login():
            raise HTTPException(status_code=401, detail="VeSync login failed")

        await manager.update()

        fans = manager.devices.air_purifiers
        if not fans:
            return JSONResponse(
                status_code=200,
                content={"status": "no_devices", "results": []},
            )

        results = []
        for fan in fans:
            try:
                await fan.reset_filter()
                results.append({"device": fan.device_name, "reset": True})
            except Exception as e:
                results.append({"device": fan.device_name, "reset": False, "error": str(e)})

    succeeded = sum(1 for r in results if r["reset"])
    failed = len(results) - succeeded

    if failed == 0:
        return JSONResponse(status_code=200, content={"status": "success", "results": results})
    if succeeded == 0:
        # Every device failed — treat as upstream failure.
        return JSONResponse(status_code=502, content={"status": "error", "results": results})
    return JSONResponse(status_code=207, content={"status": "partial", "results": results})
