class BaseLLM:
    """
    Base class for all Language Model (LLM) implementations.
    """

    def generate(self, prompt: str):
        raise NotImplementedError