from fastapi import Request


def get_client_ip(request: Request) -> str:
    """Resolve real client IP behind Nginx reverse proxy.

    X-Forwarded-For is trusted only if the request
    originated from a local proxy (127.0.0.1 / ::1).
    In production, FastAPI listens on 127.0.0.1 only
    and Nginx forwards external traffic.
    """
    remote_addr = request.client.host if request.client else "unknown"

    if remote_addr in ("127.0.0.1", "::1"):
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

    return remote_addr
