# 🚀 Task Management API

Uma API completa para gerenciamento de tarefas construída com **FastAPI**, **SQLAlchemy** e **JWT Authentication**.

## 📋 Funcionalidades

- ✅ **Autenticação JWT** com tokens Bearer
- ✅ **CRUD completo** para usuários e tarefas
- ✅ **Paginação** e filtros avançados
- ✅ **Validação de dados** com Pydantic
- ✅ **Documentação automática** com Swagger UI
- ✅ **Arquitetura limpa** (Repository + Service + Routes)
- ✅ **Permissões** - usuários só acessam suas próprias tarefas
- ✅ **Configuração flexível** com variáveis de ambiente

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **JWT** - Autenticação com tokens
- **Bcrypt** - Hash de senhas
- **MySQL** - Banco de dados
- **Uvicorn** - Servidor ASGI

## 📁 Estrutura do Projeto

```
app/
├── main.py                    # Aplicação principal
├── core/
│   ├── config.py              # Configurações da aplicação
│   └── security.py            # Autenticação e segurança
├── db/
│   ├── database.py            # Configuração do banco
│   └── models.py              # Modelos base
├── api/
│   ├── dependencies.py        # Dependências reutilizáveis
│   └── routes/
│       ├── users.py           # Rotas de usuários
│       └── tasks.py           # Rotas de tarefas
└── modules/
    ├── user/
    │   ├── model.py           # Modelo de usuário
    │   ├── schema.py          # Schemas Pydantic
    │   ├── repository.py      # Acesso aos dados
    │   └── service.py         # Lógica de negócio
    └── tasks/
        ├── model.py           # Modelo de tarefa
        ├── schema.py          # Schemas Pydantic
        ├── repository.py      # Acesso aos dados
        └── service.py         # Lógica de negócio
```

## 🚀 Instalação e Configuração

### 1. **Clonar o repositório**
```bash
git clone https://github.com/oliveirajh/Task-Managment-API.git
cd Task-Managment-API
```

### 2. **Criar ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

### 4. **Configurar variáveis de ambiente**
Criar arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/tasks_db
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Task Management API
VERSION=1.0.0
DEBUG=True
```

### 5. **Configurar banco de dados**
```sql
-- Criar banco MySQL
CREATE DATABASE tasks_db;
```

### 6. **Executar aplicação**
```bash
# Desenvolvimento
python run.py

# Ou diretamente com uvicorn
uvicorn app.main:app --reload
```

## 📚 Documentação da API

Após executar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação:

### **1. Registrar usuário**
```bash
POST /api/v1/auth/register
{
  "user": "joao",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### **2. Fazer login**
```bash
POST /api/v1/auth/login
{
  "username": "joao",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### **3. Usar token nas requisições**
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📋 Endpoints Principais

### **Usuários**
- `POST /api/v1/auth/register` - Registrar usuário
- `POST /api/v1/auth/login` - Fazer login
- `GET /api/v1/auth/me` - Obter usuário atual

### **Tarefas** (requer autenticação)
- `GET /api/v1/tasks/` - Listar tarefas (com paginação e filtros)
- `POST /api/v1/tasks/` - Criar nova tarefa
- `GET /api/v1/tasks/{id}` - Obter tarefa específica
- `PUT /api/v1/tasks/{id}` - Atualizar tarefa
- `DELETE /api/v1/tasks/{id}` - Deletar tarefa

### **Filtros e Paginação**
```bash
GET /api/v1/tasks/?page=1&size=10&status=pending&priority=high
```

## 📊 Exemplos de Uso

### **Criar uma tarefa**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Aprender sobre APIs REST",
    "priority": "high"
  }'
```

### **Listar tarefas com filtros**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?status=pending&priority=high" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Resposta:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Estudar FastAPI",
      "description": "Aprender sobre APIs REST",
      "priority": "high",
      "status": "pending",
      "user_id": 1,
      "created_at": "2025-07-16T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1,
  "size": 10
}
```

## 🗃️ Modelos de Dados

### **User**
```python
{
  "id": 1,
  "user": "joao",
  "email": "joao@example.com",
  "created_at": "2025-07-16T10:00:00"
}
```

### **Task**
```python
{
  "id": 1,
  "title": "Minha tarefa",
  "description": "Descrição da tarefa",
  "priority": "high",  # low, medium, high
  "status": "pending", # pending, in_progress, done
  "user_id": 1,
  "created_at": "2025-07-16T10:00:00"
}
```

## 🔧 Scripts Úteis

```bash
# Rodar em desenvolvimento
python run.py

```

## 🚀 Deploy

### **Docker**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Variáveis de Produção**
```env
DATABASE_URL=mysql+pymysql://user:pass@prod-db:3306/tasks_db
SECRET_KEY=super-secret-production-key
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

**João Oliveira** - [@oliveirajh](https://github.com/oliveirajh)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📚 Próximas Funcionalidades

- [ ] Comentários nas tarefas
- [ ] Categorias/Tags
- [ ] Notificações
- [ ] Upload de arquivos
- [ ] Relatórios
- [ ] API de métricas

---

**⭐ Se este projeto te ajudou, dê uma estrela no repositório!**