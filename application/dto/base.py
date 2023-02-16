from pydantic import BaseModel as Base, Field


class BaseModel(Base):
    class Config:
        orm_mode = True
        use_enum_values = True


class QueryFilterDto(BaseModel):
    """
    查询列表
    """
    page: int = 1
    size: int = 20
    keyword: str = Field(title="搜索关键字", default=None)


class ResponseSuccessDto(BaseModel):
    code: int = 200
    msg: str = "success"
