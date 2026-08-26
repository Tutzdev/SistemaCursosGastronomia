# Plataforma de Cursos de Gastronomia

Plataforma web para cursos de gastronomia, desenvolvida com **Flask, SQLAlchemy, JWT e JavaScript**, com foco em arquitetura limpa, segurança, legibilidade e facilidade de manutenção.

## Funcionalidades

* Cadastro e login de usuários
* Autenticação com JWT
* Catálogo de cursos
* Pesquisa e filtros
* Inscrição em cursos
* Área "Meus Cursos"
* Módulos e aulas
* Rotas protegidas
* Tratamento padronizado de erros
* Testes automatizados

## Tecnologias

### Backend

* Python
* Flask
* SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended
* Flask-CORS
* Argon2
* Pytest
* Ruff

### Frontend

* HTML
* CSS
* JavaScript

## Arquitetura

O backend utiliza **Application Factory**, **Blueprints** e separação de responsabilidades entre rotas, regras de negócio, persistência e configuração.

```text
Requisição
   ↓
Blueprint / Route
   ↓
Service
   ↓
SQLAlchemy
   ↓
Banco de Dados
```

Principais entidades:

```text
User
Course
Category
Module
Lesson
Enrollment
```

## Boas práticas

O projeto foi desenvolvido com foco em princípios de:

* Clean Code
* Clean Code in Python
* Effective Python
* SOLID quando aplicável
* Baixo acoplamento
* Alta coesão
* Funções pequenas e claras
* Tipagem
* Validação no backend
* Tratamento consistente de erros
* Código simples e testável

## Segurança

* Senhas protegidas com Argon2
* JWT com expiração
* Segredos em variáveis de ambiente
* Rotas protegidas
* Validação de dados no backend
* Constraints no banco
* Controle de inscrições duplicadas
* Nenhum dado sensível exposto pela API

## Principais endpoints

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

GET  /api/courses
GET  /api/courses/<id>

POST /api/courses/<id>/enroll
GET  /api/users/me/courses

GET  /api/health
```

## Executando o projeto

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

```bash
flask db upgrade
```

```bash
flask --app app:create_app run --debug
```

## Testes e qualidade

```bash
pytest
```

```bash
ruff check .
ruff format .
```

## Equipe

**Arthur — Backend**
Arquitetura Flask, autenticação, JWT, segurança, banco de dados, inscrições, integração e testes.

**Vitor — Backend**
Cursos, categorias, módulos, aulas, catálogo, pesquisa e filtros.

**Lucas — Frontend**
HTML, CSS, JavaScript e integração com a API.
