import abc
import uuid
from typing import Any, Dict

from pydantic import BaseModel, validator

from examples.models import Example
from projects.models import Project, Member
from roles.models import Role


class BaseData(BaseModel, abc.ABC):
    filename: str

    @classmethod
    def parse(cls, **kwargs):
        return cls.parse_obj(kwargs)

    def __hash__(self):
        return hash(tuple(self.dict()))

    @abc.abstractmethod
    def create(self, project: Project, meta: Dict[Any, Any]) -> Example:
        raise NotImplementedError("Please implement this method in the subclass.")


class TextData(BaseData):
    text: str

    @validator("text")
    def text_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError("is not empty.")

    def create(self, project: Project, meta: Dict[Any, Any]) -> Example:
        role = Role.objects.filter(name="annotator").first()
        members = Member.objects.filter(project=project, role=role).all()
        user = max(members, key=lambda m: m.assigned_annotation_examples.count()) if members else None
        return Example(uuid=uuid.uuid4(), project=project, filename=self.filename, assigned_to_annotator=user,
                       text=self.text, meta=meta)


class FileData(BaseData):
    def create(self, project: Project, meta: Dict[Any, Any]) -> Example:
        return Example(uuid=uuid.uuid4(), project=project, filename=self.filename, meta=meta)
