from gnews import GNews

class NewsGetter:
    def __init__(self) -> None:
        self.gnews_obj = GNews()
        self.language = ""