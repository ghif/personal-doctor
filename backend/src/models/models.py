from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

class UserQuery(BaseModel):
    query_text: Optional[str] = None
    image_data: Optional[str] = None
    input_modality: str # TEXT, SPEECH, IMAGE

class AIResponse(BaseModel):
    response_text: str
    educational_content: Optional[List[str]] = None
    triage_suggestion: str # SELF_CARE, SEE_DOCTOR, URGENT_CARE, INFO_ONLY
    disclaimer: str

class Conversation(BaseModel):
    conversation_id: str
    history: List[Union[UserQuery, AIResponse]]
    start_time: datetime
    end_time: Optional[datetime] = None
