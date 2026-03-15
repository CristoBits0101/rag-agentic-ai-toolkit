from pydantic import BaseModel


class VisionRequest(BaseModel):
    input_uri: str
