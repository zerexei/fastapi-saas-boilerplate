from server.core.exceptions import AppError


class TenancyError(AppError):
    """Base error for domain-level tenancy violations."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class TenantAccessDeniedError(TenancyError):
    def __init__(self, message: str = "Caller is not authorized for this tenant") -> None:
        super().__init__(code="TENANT_ACCESS_DENIED", message=message, status_code=403)


class TenantInactiveError(TenancyError):
    def __init__(self, message: str = "Tenant is not active") -> None:
        super().__init__(code="TENANT_INACTIVE", message=message, status_code=403)