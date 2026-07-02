from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UploadResponse(BaseModel):
    message: str
    filename: str
    uploaded_by: str
    characters_extracted: int


class AskResponse(BaseModel):
    filename: str
    question: str
    answer: str
    answered_for_user: str