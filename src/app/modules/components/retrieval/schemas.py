from pydantic import BaseModel


class RetrievalQuery(BaseModel):
    question: str


class RetrievalResult(BaseModel):
    answer: str
