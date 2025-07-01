class ApplicationException(Exception):
    """Базовое исключение для бизнес-логики приложения."""
    def __init__(self, message: str = "Ошибка бизнес-логики."):
        self.message = message
        super().__init__(message)
