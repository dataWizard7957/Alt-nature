import sentry_sdk
from app.config import settings

def init_sentry():
    if settings.SENTRY_DSN and settings.SENTRY_DSN.startswith("http"):
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            environment="hacktoberfest-2026"
        )
        print("Sentry Agent Tracing initialized successfully.")
    else:
        print("Sentry DSN not provided or invalid; running in local mode without telemetry.")