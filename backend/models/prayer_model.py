from pydantic import BaseModel

class Prayer(BaseModel):
  name: str
  time: str
  completed: bool