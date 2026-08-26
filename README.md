# Plataforma de Cursos de Gastronomia

Plataforma web desenvolvida para centralizar cursos e conteúdos voltados ao universo da gastronomia, permitindo que usuários criem suas contas, explorem cursos, realizem inscrições e acompanhem seus conteúdos através de uma área autenticada.

O projeto foi desenvolvido com foco em **simplicidade, segurança, organização e manutenção**, seguindo boas práticas de desenvolvimento e princípios de Clean Code.

---

## Funcionalidades

* Cadastro de usuários
* Login com e-mail e senha
* Autenticação utilizando JWT
* Rotas protegidas
* Área do usuário
* Catálogo de cursos
* Pesquisa de cursos
* Filtros por categoria e nível
* Página de detalhes do curso
* Organização dos cursos por módulos e aulas
* Inscrição em cursos
* Área "Meus Cursos"
* Visualização de aulas
* Controle de inscrições duplicadas
* Tratamento padronizado de erros
* API REST integrada ao frontend
* CORS configurado
* Migrations de banco de dados
* Testes automatizados

---

## Tecnologias

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended
* Flask-CORS
* Argon2
* SQLite
* Pytest
* Ruff

### Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API

---

## Arquitetura

O backend foi estruturado utilizando **Application Factory** e **Blueprints**, mantendo as responsabilidades separadas entre autenticação, usuários, cursos e inscrições.

```text
backend/
├── app/
│   ├── auth/
│   ├── users/
│   ├── courses/
│   ├── enrollments/
│   ├── models/
│   ├── errors/
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
│
├── migrations/
├── tests/
├── .env.example
├── requirements.txt
└── run.py
```

---

## Fluxo principal

```text
Cadastro
   ↓
Login
   ↓
Autenticação JWT
   ↓
Catálogo de cursos
   ↓
Detalhes do curso
   ↓
Inscrição
   ↓
Meus Cursos
   ↓
Módulos e aulas
```

---

## Autenticação

A autenticação da aplicação utiliza **JSON Web Tokens (JWT)**.

Após realizar login, o usuário recebe um `access_token` que deve ser enviado nas requisições protegidas.

```http
Authorization: Bearer <access_token>
```

As senhas dos usuários nunca são armazenadas em texto puro.

O projeto utiliza **Argon2** para geração e validação segura dos hashes das senhas.

---

## Principais endpoints

### Cadastro

```http
POST /api/auth/register
```

```json
{
  "name": "Arthur",
  "email": "arthur@example.com",
  "password": "senha-segura",
  "password_confirmation": "senha-segura"
}
```

---

### Login

```http
POST /api/auth/login
```

```json
{
  "email": "arthur@example.com",
  "password": "senha-segura"
}
```

---

### Usuário autenticado

```http
GET /api/auth/me
Authorization: Bearer <token>
```

---

### Listar cursos

```http
GET /api/courses
```

---

### Visualizar curso

```http
GET /api/courses/<course_id>
```

---

### Inscrever-se em um curso

```http
POST /api/courses/<course_id>/enroll
Authorization: Bearer <token>
```

---

### Meus cursos

```http
GET /api/users/me/courses
Authorization: Bearer <token>
```

---

### Health Check

```http
GET /api/health
```

Resposta:

```json
{
  "status": "ok"
}
```

---

## Banco de dados

O MVP utiliza **SQLite** através do SQLAlchemy.

As principais entidades são:

```text
User
Course
Category
Module
Lesson
Enrollment
```

### Relacionamentos

```text
User
 └── Enrollments
       └── Course
             ├── Category
             └── Modules
                   └── Lessons
```

Cada usuário pode possuir várias inscrições e cada curso pode possuir vários alunos.

A combinação entre usuário e curso possui uma restrição única, impedindo inscrições duplicadas.

---

## Configuração

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre no projeto:

```bash
cd <NOME_DO_REPOSITORIO>
```

Crie o ambiente virtual:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`.

```env
APP_ENV=development
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=60
CORS_ALLOWED_ORIGINS=http://localhost:5500
```

Nunca utilize a chave de exemplo em produção.

---

## Migrations

Inicialize ou atualize o banco:

```bash
flask db upgrade
```

Para criar uma nova migration:

```bash
flask db migrate -m "migration description"
```

Aplicar:

```bash
flask db upgrade
```

---

## Executando o backend

```bash
flask --app app:create_app run --debug
```

Por padrão:

```text
http://127.0.0.1:5000
```

---

## Testes

O projeto possui testes automatizados utilizando Pytest.

Execute:

```bash
pytest
```

Os testes cobrem principalmente:

* cadastro;
* autenticação;
* JWT;
* usuários;
* inscrições;
* validações;
* permissões;
* tratamento de erros;
* integridade dos dados.

---

## Qualidade de código

O projeto utiliza Ruff para lint e formatação.

### Verificar código

```bash
ruff check .
```

### Formatar

```bash
ruff format .
```

---

## Segurança

Algumas práticas adotadas no projeto:

* Senhas protegidas com Argon2
* JWT com expiração
* Segredos armazenados em variáveis de ambiente
* Rotas privadas protegidas
* Validação de dados no backend
* Controle de inscrições duplicadas
* IDs de usuário obtidos pelo JWT
* Tratamento padronizado de erros
* Ausência de dados sensíveis nas respostas
* CORS configurado
* Constraints no banco de dados

O backend nunca confia exclusivamente nas informações enviadas pelo frontend.

---

## Princípios de desenvolvimento

O projeto foi desenvolvido seguindo conceitos encontrados em:

* Clean Code
* Clean Code in Python
* Effective Python
* How to Be a Programmer

Com foco em:

* código legível;
* funções pequenas e claras;
* baixo acoplamento;
* alta coesão;
* responsabilidade única;
* simplicidade;
* testabilidade;
* segurança;
* facilidade de manutenção.

---

## Equipe

### Arthur

Backend

* Arquitetura Flask
* Autenticação
* JWT
* Segurança
* Usuários
* Inscrições
* Banco de dados
* Integração
* Testes

### Vitor

Backend

* Cursos
* Categorias
* Módulos
* Aulas
* Catálogo
* Pesquisa
* Filtros

### Lucas

Frontend

* HTML
* CSS
* JavaScript
* Interface
* Integração com API
* Experiência do usuário

---

## Status

**MVP concluído e funcional.**

O sistema possui o fluxo principal completo:

```text
Criar conta
→ Entrar
→ Explorar cursos
→ Visualizar curso
→ Inscrever-se
→ Acessar Meus Cursos
→ Visualizar aulas
```

---

## Próximas versões

A arquitetura foi preparada para expansão futura com funcionalidades como:

* Login com Google
* Gateway de pagamento
* Cursos pagos
* Histórico de compras
* Perfis de instrutores
* Certificados
* Avaliações
* Progresso de aulas
* Dashboard administrativo

---

## Licença

Projeto desenvolvido para fins acadêmicos e de demonstração.
