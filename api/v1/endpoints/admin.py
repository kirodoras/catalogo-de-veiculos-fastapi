from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Header
from dotenv import load_dotenv
import os

load_dotenv()

admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')
secret_key = os.getenv('SECRET_KEY')

router = APIRouter()

# Configuração básica de autenticação
SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para gerar um token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota para autenticar e gerar o token JWT
@router.post("/token")
async def login_token(username: str, password: str):
    # Verifica se as credenciais fornecidas correspondem ao usuário admin
    if username == admin_username and password == admin_password:
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Função de validação do token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.JWTError:
        return False

# Função que requer autenticação com JWT para validação do token
async def verifica_token(authorization: str):
    print(authorization)
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    if authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        raise HTTPException(
            status_code=401, detail="A autenticação deve ser do tipo Bearer")

    token_valid = verify_token(token)
    if token_valid:
        return {"message": "Token válido"}
    else:
        raise HTTPException(status_code=401, detail="Token inválido")