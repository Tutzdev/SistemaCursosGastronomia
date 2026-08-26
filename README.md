# Curso Gastronômico — backend do MVP

Backend Flask responsável por autenticação, usuários e inscrições. O catálogo
de cursos pertence ao módulo de Vitor e é consumido pela integração com a tabela
`courses`.

## Preparação

Requer Python 3.11 ou superior.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install ".[dev]"
Copy-Item .env.example .env
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate` e copie o
arquivo com `cp .env.example .env`.

Preencha `JWT_SECRET_KEY` no `.env` com um segredo aleatório. Um valor pode ser
gerado localmente com:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Variáveis disponíveis:

- `APP_ENV`: ambiente da aplicação;
- `DATABASE_URL`: URL SQLAlchemy, `sqlite:///app.db` no MVP;
- `JWT_SECRET_KEY`: segredo obrigatório, sem valor padrão;
- `JWT_ACCESS_TOKEN_EXPIRES_MINUTES`: validade do token, padrão 60;
- `CORS_ALLOWED_ORIGINS`: origens explícitas separadas por vírgula.

## Banco e execução

```powershell
flask --app app:create_app db upgrade
flask --app app:create_app run --debug
```

A API estará em `http://127.0.0.1:5000`. O health check é
`GET /api/health`. Os demais contratos estão em [docs/api.md](docs/api.md).

## Qualidade

```powershell
ruff format --check .
ruff check .
pytest
```

Os testes usam um SQLite em memória separado e definem um model `Course`
exclusivamente em `tests/`. Em produção, nenhuma implementação falsa de curso é
criada.

## Integração com o catálogo

O model real do catálogo deve usar a tabela `courses`, chave primária inteira
`id` e expor os campos públicos `title`, `description`, `thumbnail_url` e
`level`. Após o model de Vitor ser adicionado, ele também deve ser importado na
inicialização da aplicação para que o Flask-Migrate enxergue seus metadados.
"# SistemaCursosGastronomia" 
