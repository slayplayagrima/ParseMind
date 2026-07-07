from pydantic import BaseModel, Field


class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    location: str


class Education(BaseModel):
    degree: str
    institution: str
    start_year: int | None = None
    end_year: int | None = None


class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str


class Project(BaseModel):
    name: str
    description: str


class ResumeResponse(BaseModel):
    candidate: Candidate

    summary: str

    education: list[Education]

    experience: list[Experience]

    projects: list[Project]

    skills: list[str]

    certifications: list[str]

    strengths: list[str]

    improvements: list[str]

    ats_score: int = Field(ge=0, le=100)