def news_feed_prompt(title : str, content : str) -> str:
    return f"""
            News Title: {title}
            News Content: {content}
        """

def gnews_keywords_prompt(question: str, title: str = '', key_points: list[str] = [], number_gnews_keyword : int = 3) -> str:
    return f"""
        You are provided with a context and a question based on this context.
        Your task is to generate a list of {number_gnews_keyword} keywords that will be send to gnews api to retrieve the relevant articles which will allow to respond to the question. 
        The keywords MUST be efficient to give information directly related to the question in its context. 
        
        Context: {key_points}
        Question: {question}
        """
        
def question_answering_prompt(context : str, question : str) -> str:
    return f"""

        Context: {context}
        Question: {question}
        """
    