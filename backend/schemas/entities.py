from pydantic import BaseModel


class EntityResponse(BaseModel):
    people: list[str]
    organizations: list[str]
    emails: list[str]
    phones: list[str]
    locations: list[str]
    dates: list[str]
    money: list[str]
    skills: list[str]
    technologies: list[str]