### Catálogo de Veículos - FastAPI

Este é um backend desenvolvido em Python usando FastAPI, que oferece funcionalidades para um CRUD (Create, Read, Update, Delete) de veículos, juntamente com rotas de autorização.

#### Configuração do Banco de Dados
1. **PostgreSQL como Banco de Dados**
   - [Download do PostgreSQL para Ubuntu](https://www.postgresql.org/download/linux/ubuntu/)
   - [Pgadmin - Ferramenta para gerenciar databases](https://www.pgadmin.org/download/pgadmin-4-apt/)

2. **Criar Database e Configurar a Variável de Ambiente DB_URL**
   - Estrutura: `postgresql+asyncpg://username:password@localhost:5432/database`
   - Exemplo: `postgresql+asyncpg://postgres:kiro@localhost:5432/veiculos`

3. **Arquivo .env**
   - Crie um arquivo `.env` com as seguintes variáveis seguindo o `.env.example`:
     ```
     DB_URL=postgresql+asyncpg://postgres:kiro@localhost:5432/veiculos
     ADMIN_USERNAME=admin
     ADMIN_PASSWORD=admin
     SECRET_KEY=secret
     ```

#### Instalação e Execução do Projeto
4. **Verificar a Instalação do pip**
   - `pip --version`

5. **Ambiente Virtual (Opcional)**
   - Crie um ambiente virtual usando `virtualenv` e `virtualenvwrapper`.

6. **Instalar Dependências e Rodar o Projeto**
   - No diretório principal (que contém `main.py`):
     ```
     pip install -r requirements.txt  # Instalar dependências
     python criar_tabelas.py          # Criar tabelas no banco de dados  
     python main.py                   # Rodar o projeto
     ```

#### Rotas de Gerenciamento de Veículos
- `GET /api/v1/veiculos/`: Recupera todos os registros de veículos.
- Exemplo de Requisição:
    ```
    GET http://localhost:8000/api/v1/veiculos/
    ```
- `GET /api/v1/veiculos/{Veiculo_id}`: Recupera os detalhes de um veículo específico com base no ID.
- Exemplo de Requisição:
    ```
    GET http://localhost:8000/api/v1/veiculos/1
    PATH:{Veiuclo_id}
    ```
- `POST /api/v1/veiculos/`: Cria um novo registro de veículo. (Rota protegida)
- Exemplo de Requisição:
    ```
    POST http://localhost:8000/api/v1/veiculos/
    HEADER: x-authorization: Bearer {token}
    BODY: {
        "nome": "Fusca",
        "marca": "Volkswagen",
        "modelo": "Fusco",
        "foto": "https://...",
    }
    ```
- `PUT /{Veiculo_id}`: Atualiza os detalhes de um veículo específico com base no ID. (Rota protegida)
- Exemplo de Requisição:
    ```
    PUT http://localhost:8000/api/v1/veiculos/1
    PATH:{Veiuclo_id}
    HEADER: x-authorization: Bearer {token}
    BODY: {
        "nome": "Fusca",
        "marca": "Volkswagen",
        "modelo": "Fusco",
        "foto": "https://...",
    }
    ```
- `DELETE /{Veiculo_id}`: Remove um veículo específico com base no ID. (Rota protegida)
- Exemplo de Requisição:
    ```
    DELETE http://localhost:8000/api/v1/veiculos/1
    PATH:{Veiuclo_id}
    HEADER: x-authorization: Bearer {token}
    ```

#### Rotas de Autenticação e Verificação de Token
- `POST /token`: Rota para autenticação e geração de um token JWT.
   - Exemplo de Requisição:
    ```
    POST http://localhost:8000/api/v1/admin/token?username=admin&password=admin
    ```