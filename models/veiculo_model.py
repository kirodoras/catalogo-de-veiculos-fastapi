from typing import Optional

from sqlmodel import Field, SQLModel


class VeiculoModel(SQLModel, table=True):
    __tablename__: str = 'veiculos'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    marca: str
    modelo: str
    foto: str

