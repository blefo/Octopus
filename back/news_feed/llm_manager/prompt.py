def rephrase_title(news_title: str, news_content: str):
    return f"""
    You are provided with a news title and content and your task is to rephrase it.
    You MUST make if very short.
    You MUST make it as much informative as possible.
    You MSUT make it a little catchy.

    News title: {news_title}
    News content: {news_content}
    """