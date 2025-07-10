class ProviderError(Exception): ...


class FetchingError(ProviderError):
    def __init__(self, code: str, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnexpectedResponseError(ProviderError):
    def __init__(self, response_text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
