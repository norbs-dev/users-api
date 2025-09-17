from typing import Optional
from datetime import datetime
from pydantic import BaseModel



class ResponseBody(BaseModel):
    timestamp: str = datetime.now().isoformat()
    execution_time_ms: float = 0
    logins: Optional[list] = None
    teams: Optional[list] = None
    countries: Optional[list] = None
    data: Optional[list] = None

class Response(BaseModel):
    status: int
    body: ResponseBody