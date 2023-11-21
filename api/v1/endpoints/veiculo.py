from typing import List

from fastapi import APIRouter, Header
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from api.v1.endpoints.admin import verifica_token

from models.veiculo_model import VeiculoModel
from core.deps import get_session

from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  
Select.inherit_cache = True  


router = APIRouter()


# POST Veiculo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=VeiculoModel)
async def post_Veiculo(Veiculo: VeiculoModel, db: AsyncSession = Depends(get_session), x_authorization: str = Header(default=None)):
    await verifica_token(x_authorization)
    novo_Veiculo = VeiculoModel(nome=Veiculo.nome, 
                                marca=Veiculo.marca,
                                modelo=Veiculo.modelo,
                                foto=Veiculo.foto)

    db.add(novo_Veiculo)
    await db.commit()

    return novo_Veiculo


# GET Veiculos
@router.get('/', response_model=List[VeiculoModel])
async def get_Veiculos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel)
        result = await session.execute(query)
        Veiculos: List[VeiculoModel] = result.scalars().all()

        return Veiculos


# GET Veiculo
@router.get('/{Veiculo_id}', response_model=VeiculoModel, status_code=status.HTTP_200_OK)
async def get_Veiculo(Veiculo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.id == Veiculo_id)
        result = await session.execute(query)
        Veiculo: VeiculoModel = result.scalar_one_or_none()

        if Veiculo:
            return Veiculo
        else:
            raise HTTPException(detail='Veiculo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Veiculo
@router.put('/{Veiculo_id}', status_code=status.HTTP_202_ACCEPTED, response_model=VeiculoModel)
async def put_Veiculo(Veiculo_id: int, Veiculo: VeiculoModel, db: AsyncSession = Depends(get_session), x_authorization: str = Header(default=None)):
    await verifica_token(x_authorization)
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.id == Veiculo_id)
        result = await session.execute(query)
        Veiculo_up: VeiculoModel = result.scalar_one_or_none()

        if Veiculo_up:
            Veiculo_up.nome = Veiculo.nome
            Veiculo_up.marca = Veiculo.marca
            Veiculo_up.modelo = Veiculo.modelo
            Veiculo_up.foto = Veiculo.foto

            await session.commit()

            return Veiculo_up
        else:
            raise HTTPException(detail='Veiculo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Veiculo
@router.delete('/{Veiculo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_Veiculo(Veiculo_id: int, db: AsyncSession = Depends(get_session), x_authorization: str = Header(default=None)):
    await verifica_token(x_authorization)
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.id == Veiculo_id)
        result = await session.execute(query)
        Veiculo_del: VeiculoModel = result.scalar_one_or_none()

        if Veiculo_del:
            await session.delete(Veiculo_del)
            await session.commit()

            # Colocamos por conta de um bug no FastAPI
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Veiculo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
