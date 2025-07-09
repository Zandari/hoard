class ProviderError(Exception): ...


class FetchingError(ProviderError):
    def __name__(code: int | str, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnexpectedResponseError(ProviderError):
    def __name__(response_text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
