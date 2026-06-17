from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import hello_auth, profile, fir, bot, search, sos
from app.core.config import settings

app = FastAPI(title="Safe-sphere Backend")

# Configure CORS
origins = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_origin_regex=r"https://safe-sphere-.*\.vercel\.app",
    allow_credentials=True if origins else False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Exception Handlers
@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    print(f"GLOBAL ERROR: {str(exc)}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": str(exc)}
    )

# Include Routers
app.include_router(hello_auth.router, tags=["General"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(fir.router, prefix="/api/fir", tags=["FIR Forms"])
app.include_router(bot.router, prefix="/api/bot", tags=["Bot"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(sos.router, prefix="/api/sos", tags=["SOS"])
app.include_router(sos.router, prefix="/api/police", tags=["Police"])
app.include_router(sos.router, prefix="/api/crime", tags=["Crime"])
