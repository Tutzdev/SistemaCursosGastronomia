# AGENTS.md

## 1. Objetivo deste arquivo

Este documento define as regras obrigatórias para qualquer agente de IA que trabalhe no backend do MVP.

O agente deve produzir um código:

* correto;
* seguro;
* simples de compreender;
* fácil de testar;
* fácil de manter;
* consistente com o restante do projeto;
* preparado para integração com o frontend;
* sem complexidade desnecessária;
* com baixo risco de regressões.

As decisões devem seguir os princípios apresentados em:

* Clean Code;
* Clean Code in Python;
* Effective Python;
* How to Be a Programmer;
* boas práticas modernas de engenharia de software.

Este arquivo tem prioridade sobre sugestões genéricas do agente.

Quando houver conflito entre rapidez e qualidade, o agente deve buscar a solução mais simples que continue correta, segura e testável.

---

# 2. Escopo de responsabilidade

Este agente trabalhará exclusivamente na parte de Arthur no MVP.

## Responsabilidades de Arthur

* estrutura inicial do backend;
* configuração da aplicação;
* configuração do banco de dados;
* autenticação;
* cadastro de usuários;
* login com e-mail e senha;
* geração e validação de JWT;
* hash seguro de senha;
* identificação do usuário autenticado;
* proteção de rotas;
* inscrição do aluno em cursos;
* listagem dos cursos do usuário;
* configuração de CORS;
* tratamento padronizado de erros;
* integração dos módulos desenvolvidos por outros membros;
* testes da própria responsabilidade;
* preparação do backend para demonstração.

## Fora do escopo neste momento

Não implementar agora:

* login com Google;
* pagamentos;
* gateway de pagamento;
* Mercado Pago;
* recuperação de senha;
* confirmação de e-mail;
* certificados;
* avaliações;
* comentários;
* cupons;
* upload de vídeos;
* processamento de vídeos;
* notificações;
* microsserviços;
* mensageria;
* cache distribuído;
* aplicativo mobile;
* recursos financeiros;
* funcionalidades que não façam parte do MVP.

Não antecipar funcionalidades futuras sem uma solicitação explícita.

---

# 3. Stack do MVP

O backend deve utilizar:

* Python;
* FastAPI;
* SQLAlchemy;
* Pydantic;
* SQLite no ambiente do MVP;
* JWT para autenticação;
* biblioteca confiável para hash de senha;
* Pytest para testes;
* Ruff para lint e formatação;
* Alembic para migrations, quando configurado no projeto.

Não criar um segundo backend em Java.

Não introduzir frameworks adicionais sem necessidade real.

Não substituir bibliotecas existentes sem justificar tecnicamente e sem verificar os impactos.

---

# 4. Regra principal de implementação

Antes de modificar qualquer arquivo, o agente deve:

1. examinar a estrutura atual do repositório;
2. ler os arquivos relacionados à tarefa;
3. identificar padrões já utilizados;
4. verificar contratos de API existentes;
5. verificar models, schemas e dependências existentes;
6. verificar testes existentes;
7. evitar duplicar implementações;
8. planejar a menor alteração capaz de concluir corretamente a tarefa.

O agente nunca deve presumir que um arquivo está vazio ou que uma funcionalidade não existe sem verificar primeiro.

O agente não deve reescrever módulos inteiros quando uma alteração localizada for suficiente.

---

# 5. Princípios obrigatórios

## 5.1 Simplicidade

Escolha a solução mais simples que satisfaça completamente o requisito.

Evite:

* abstrações prematuras;
* classes sem necessidade;
* heranças desnecessárias;
* factories sem benefício concreto;
* múltiplas camadas sem responsabilidade real;
* padrões de projeto utilizados apenas por estética;
* código genérico para situações que ainda não existem.

Não crie uma arquitetura de grande empresa para um MVP.

Simplicidade não significa colocar toda a lógica em um único arquivo.

## 5.2 Responsabilidade única

Cada função, classe e módulo deve possuir uma responsabilidade clara.

Exemplos:

* rota recebe e devolve dados HTTP;
* service executa regras de negócio;
* repository acessa o banco;
* schema valida entrada e saída;
* model representa persistência;
* dependency resolve autenticação e recursos da aplicação;
* configuração lê variáveis de ambiente.

Não colocar regras de negócio diretamente nas rotas.

Não colocar detalhes HTTP dentro dos repositories.

Não colocar consultas SQL dentro dos schemas.

## 5.3 Clareza

O código deve ser compreendido sem exigir explicações externas.

Utilize nomes descritivos.

Preferir:

```python
get_user_by_email
create_access_token
verify_password
enroll_user_in_course
get_current_user
```

Evitar:

```python
get_data
do_auth
process
handle
execute_task
func1
obj
x
temp
```

Nomes devem expressar intenção.

## 5.4 Funções pequenas e focadas

Uma função deve realizar uma ação principal.

Divida uma função quando ela:

* valida dados;
* consulta o banco;
* aplica regras;
* transforma resultados;
* monta respostas;
* trata diferentes responsabilidades ao mesmo tempo.

Não dividir funções apenas para reduzir linhas artificialmente.

A separação deve melhorar a leitura, os testes ou o reaproveitamento.

## 5.5 Fluxo legível

Utilize retornos antecipados para evitar níveis excessivos de indentação.

Preferir:

```python
if user is None:
    raise InvalidCredentialsError()

if not verify_password(password, user.password_hash):
    raise InvalidCredentialsError()

return create_access_token(user.id)
```

Evitar estruturas profundamente aninhadas.

## 5.6 Não repetir conhecimento

Não duplicar:

* regras de senha;
* leitura de token;
* normalização de e-mail;
* criação de sessão;
* construção de erros;
* consulta do usuário atual;
* regras de inscrição.

Extraia código repetido somente quando a duplicação representar o mesmo conhecimento ou a mesma regra.

Não crie abstrações apenas porque duas funções possuem algumas linhas parecidas.

---

# 6. Idioma e convenções

## Código

Todos os identificadores do código devem ser escritos em inglês:

* nomes de arquivos;
* variáveis;
* funções;
* classes;
* models;
* schemas;
* services;
* repositories;
* enums.

## Mensagens apresentadas ao usuário

Mensagens de erro da API podem ser escritas em português, desde que sejam consistentes.

## Convenções Python

* utilizar `snake_case` para funções, variáveis e módulos;
* utilizar `PascalCase` para classes;
* utilizar `UPPER_SNAKE_CASE` para constantes;
* utilizar imports absolutos dentro do projeto;
* utilizar type hints;
* evitar argumentos mutáveis como valor padrão;
* utilizar `pathlib.Path` no lugar de manipulação manual de caminhos;
* utilizar enums para conjuntos fechados de valores;
* utilizar `datetime` com timezone quando datas forem necessárias.

---

# 7. Estrutura recomendada

A estrutura pode ser ajustada ao projeto existente, mas as responsabilidades devem permanecer separadas.

```text
backend/
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── token.py
│   ├── users/
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── enrollments/
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── shared/
│   │   └── schemas.py
│   └── main.py
├── tests/
│   ├── integration/
│   ├── unit/
│   └── conftest.py
├── .env.example
├── pyproject.toml
└── README.md
```

Não reorganizar o projeto caso já exista uma estrutura coerente.

---

# 8. Arquitetura das requisições

O fluxo preferencial é:

```text
HTTP request
→ router
→ service
→ repository
→ database
```

E na resposta:

```text
database
→ repository
→ service
→ response schema
→ HTTP response
```

## Router

O router deve:

* receber parâmetros;
* validar entrada por meio de schemas;
* resolver dependencies;
* chamar o service;
* declarar status HTTP;
* declarar schema de resposta.

O router não deve:

* executar hash de senha;
* consultar diretamente o banco;
* criar JWT diretamente;
* aplicar regras de inscrição;
* conter lógica extensa;
* capturar exceções genéricas.

## Service

O service deve:

* aplicar regras de negócio;
* coordenar repositories;
* validar estados;
* lançar exceções de domínio;
* definir o comportamento da funcionalidade.

## Repository

O repository deve:

* executar consultas;
* adicionar entidades;
* atualizar entidades;
* remover entidades quando necessário;
* abstrair detalhes da persistência.

O repository não deve decidir regras de negócio.

## Schemas

Os schemas devem:

* validar entradas;
* definir respostas;
* impedir exposição de campos sensíveis;
* manter contratos claros.

Nunca retornar models SQLAlchemy diretamente sem uma resposta validada.

---

# 9. Configuração da aplicação

Toda configuração variável deve vir do ambiente.

Exemplos:

```env
APP_ENV=development
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
CORS_ALLOWED_ORIGINS=
```

## Regras

* nunca colocar segredos reais no código;
* nunca versionar `.env`;
* manter `.env.example` sem credenciais;
* não criar uma chave JWT insegura como fallback de produção;
* falhar de forma clara quando uma configuração obrigatória estiver ausente;
* centralizar configurações em um único módulo;
* não espalhar chamadas a `os.getenv` pela aplicação;
* validar tipos das configurações;
* separar configurações de testes das configurações normais.

Valores padrão só devem existir quando forem seguros.

---

# 10. Banco de dados

## Sessão

A sessão do banco deve:

* possuir ciclo de vida controlado;
* ser fechada corretamente;
* ser fornecida por dependency;
* realizar rollback quando uma operação falhar;
* evitar sessões globais compartilhadas entre requisições.

## Transações

Operações compostas devem ser atômicas.

Exemplo de inscrição:

1. verificar se o curso existe;
2. verificar se a inscrição já existe;
3. criar a inscrição;
4. confirmar a transação.

Se uma etapa falhar, a operação não deve deixar dados incompletos.

## Constraints

Regras importantes também devem existir no banco.

Exemplos:

* e-mail único;
* combinação `user_id + course_id` única em inscrições;
* campos obrigatórios como `nullable=False`;
* foreign keys corretamente definidas;
* índices em campos pesquisados com frequência.

A aplicação deve tratar violações de constraint de forma previsível.

Não confiar apenas em uma consulta anterior para impedir duplicidade, pois duas requisições podem ocorrer simultaneamente.

## Migrations

Quando Alembic estiver configurado:

* toda alteração de schema deve possuir migration;
* migrations devem ser pequenas e revisáveis;
* não editar migration já aplicada sem necessidade;
* verificar upgrade e downgrade quando aplicável.

`create_all` pode ser utilizado em testes isolados, mas não deve substituir migrations em ambientes persistentes.

---

# 11. Model de usuário

O usuário deve possuir, no mínimo:

```text
id
name
email
password_hash
role
created_at
```

## Regras

* o e-mail deve ser único;
* o e-mail deve ser normalizado antes da consulta e do armazenamento;
* a senha nunca deve ser armazenada em texto puro;
* `password_hash` nunca deve aparecer em respostas;
* novos usuários do MVP devem receber o papel `STUDENT`;
* o papel não deve ser aceito livremente no cadastro público;
* não permitir que um usuário se cadastre como administrador;
* datas devem ser geradas pelo backend;
* IDs devem ser gerados de maneira consistente com o projeto.

---

# 12. Cadastro

Endpoint esperado:

```http
POST /auth/register
```

Entrada mínima:

```json
{
  "name": "Arthur",
  "email": "arthur@example.com",
  "password": "senha-segura",
  "password_confirmation": "senha-segura"
}
```

## Regras do cadastro

* remover espaços desnecessários do nome;
* normalizar o e-mail;
* validar formato do e-mail;
* comparar senha e confirmação;
* validar tamanho mínimo e máximo da senha;
* verificar e-mail duplicado;
* gerar hash com biblioteca confiável;
* criar usuário como `STUDENT`;
* nunca registrar a senha em logs;
* nunca devolver a senha;
* nunca devolver o hash.

O backend deve ser a autoridade final das validações, mesmo que o frontend valide os mesmos campos.

## E-mail duplicado

Responder com status apropriado, preferencialmente:

```http
409 Conflict
```

A resposta deve possuir um código de erro estável.

---

# 13. Login

Endpoint esperado:

```http
POST /auth/login
```

Entrada:

```json
{
  "email": "arthur@example.com",
  "password": "senha-segura"
}
```

Saída esperada:

```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

## Regras

* normalizar o e-mail;
* localizar o usuário;
* verificar a senha com biblioteca confiável;
* gerar JWT somente após autenticação válida;
* utilizar expiração;
* incluir identificador estável do usuário no subject do token;
* não incluir senha ou dados sensíveis no token;
* não diferenciar publicamente “e-mail inexistente” de “senha incorreta”;
* não registrar credenciais;
* não aceitar algoritmo informado pelo cliente.

Mensagem pública recomendada:

```text
E-mail ou senha inválidos.
```

---

# 14. Segurança de senha

Nunca implementar algoritmo de hash manualmente.

Utilizar uma biblioteca confiável com um algoritmo moderno de hash de senha, preferencialmente Argon2id ou equivalente seguro e mantido.

## Regras obrigatórias

* nunca utilizar MD5;
* nunca utilizar SHA puro para senhas;
* nunca utilizar Base64 como proteção;
* nunca criptografar senha para recuperá-la depois;
* nunca armazenar senha;
* nunca retornar hash;
* nunca imprimir senha;
* nunca incluir senha em exceções;
* nunca incluir senha em fixtures públicas.

A função de hash e a função de verificação devem ficar centralizadas.

Exemplo de interface:

```python
def hash_password(password: str) -> str: ...


def verify_password(password: str, password_hash: str) -> bool: ...
```

---

# 15. JWT

A implementação de JWT deve ser pequena e isolada.

Exemplo de interface:

```python
def create_access_token(subject: str) -> str: ...


def decode_access_token(token: str) -> TokenPayload: ...
```

## O token deve conter

* `sub`: identificador do usuário;
* `exp`: data de expiração;
* `iat`, quando utilizado consistentemente.

## O token não deve conter

* senha;
* hash da senha;
* segredo;
* informações desnecessárias;
* dados que o usuário possa alterar e que sejam críticos para autorização.

## Validação

A aplicação deve rejeitar:

* token expirado;
* token malformado;
* assinatura inválida;
* token sem subject;
* subject em formato inválido;
* usuário removido ou inexistente.

Falhas de autenticação devem responder preferencialmente com:

```http
401 Unauthorized
```

Com header:

```http
WWW-Authenticate: Bearer
```

---

# 16. Usuário autenticado

Endpoint esperado:

```http
GET /auth/me
```

O endpoint deve:

* exigir token;
* validar token;
* localizar o usuário atual;
* retornar apenas dados públicos.

Exemplo:

```json
{
  "id": 1,
  "name": "Arthur",
  "email": "arthur@example.com",
  "role": "STUDENT",
  "created_at": "2026-08-25T18:00:00Z"
}
```

A resolução do usuário atual deve ser feita por uma dependency reutilizável.

Exemplo:

```python
def get_current_user(...) -> User:
    ...
```

Não duplicar a leitura do token em cada rota.

---

# 17. Inscrição em cursos

Endpoint esperado:

```http
POST /courses/{course_id}/enroll
```

O endpoint deve ser protegido.

## Regras

* o usuário precisa estar autenticado;
* o curso precisa existir;
* o usuário não pode possuir duas inscrições no mesmo curso;
* a inscrição deve registrar usuário, curso e data;
* o backend deve ignorar qualquer `user_id` enviado pelo cliente;
* o usuário deve ser obtido pelo JWT;
* a restrição de duplicidade deve existir também no banco;
* erros de concorrência devem ser tratados.

Não criar um segundo model de curso.

O domínio de cursos pertence ao módulo desenvolvido pelo responsável pelo catálogo.

A implementação deve importar e utilizar o model ou interface existente de cursos.

Se o módulo de cursos ainda não estiver disponível durante testes unitários, utilizar fakes ou mocks somente nos testes.

Não adicionar classes falsas de curso ao código de produção.

## Curso inexistente

Responder preferencialmente com:

```http
404 Not Found
```

## Inscrição duplicada

Responder preferencialmente com:

```http
409 Conflict
```

---

# 18. Meus cursos

Endpoint esperado:

```http
GET /users/me/courses
```

O endpoint deve:

* exigir autenticação;
* utilizar o usuário do JWT;
* retornar somente cursos vinculados ao usuário;
* não aceitar `user_id` na URL ou no corpo;
* retornar uma lista vazia quando não houver inscrições;
* utilizar schemas de resposta;
* evitar consultas N+1.

A resposta deve ser compatível com o contrato do frontend.

Não inventar formatos diferentes para o mesmo curso em cada endpoint sem necessidade.

---

# 19. Integração com o módulo de cursos

O domínio de Arthur não deve duplicar responsabilidades de Vitor.

Arthur pode depender de:

* `Course`;
* consultas de existência do curso;
* consulta dos dados públicos do curso;
* relacionamentos necessários para listar inscrições.

Arthur não deve recriar:

* `Category`;
* `Course`;
* `Module`;
* `Lesson`;
* pesquisa de cursos;
* filtros do catálogo;
* regras internas de criação de cursos.

Quando uma integração estiver incompleta:

1. identificar claramente a interface necessária;
2. manter o código desacoplado;
3. utilizar mocks somente em testes;
4. não inserir implementações temporárias silenciosas em produção;
5. documentar a dependência de integração.

---

# 20. CORS

O CORS deve permitir somente os endereços necessários ao frontend.

## Regras

* ler origens permitidas pela configuração;
* não utilizar `*` com credenciais;
* não liberar métodos e headers sem necessidade quando houver configuração específica;
* permitir o header `Authorization`;
* manter configuração diferente entre desenvolvimento e produção;
* não corrigir erro de CORS desabilitando segurança indiscriminadamente.

Exemplo de origens no desenvolvimento:

```text
http://localhost:3000
http://127.0.0.1:3000
http://localhost:5500
http://127.0.0.1:5500
```

Utilizar apenas as origens realmente usadas pelo projeto.

---

# 21. Tratamento de erros

A aplicação deve possuir respostas de erro consistentes.

Formato recomendado:

```json
{
  "error": {
    "code": "EMAIL_ALREADY_REGISTERED",
    "message": "Já existe uma conta com este e-mail.",
    "details": null
  }
}
```

## Códigos de erro

Os códigos devem ser:

* estáveis;
* escritos em inglês;
* independentes da mensagem;
* úteis para o frontend.

Exemplos:

```text
VALIDATION_ERROR
EMAIL_ALREADY_REGISTERED
INVALID_CREDENTIALS
INVALID_TOKEN
TOKEN_EXPIRED
AUTHENTICATION_REQUIRED
USER_NOT_FOUND
COURSE_NOT_FOUND
ALREADY_ENROLLED
INTERNAL_ERROR
```

## Exceções

Criar exceções de domínio quando elas melhorarem a clareza.

Exemplos:

```python
class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class AlreadyEnrolledError(Exception):
    pass
```

Não usar `except Exception` para esconder problemas.

Uma captura genérica só é aceitável na camada global da aplicação para:

* registrar o erro;
* devolver uma resposta interna segura;
* preservar o traceback nos logs;
* impedir exposição de detalhes internos.

Nunca responder ao cliente com traceback, caminho de arquivo, query SQL ou segredo.

---

# 22. Status HTTP

Utilizar os status de forma consistente.

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
500 Internal Server Error
```

Regras gerais:

* cadastro criado: `201`;
* login válido: `200`;
* usuário atual: `200`;
* inscrição criada: `201`;
* e-mail duplicado: `409`;
* inscrição duplicada: `409`;
* credenciais inválidas: `401`;
* token inválido: `401`;
* curso inexistente: `404`;
* validação de entrada: `422` ou padrão consistente definido pelo projeto.

Não retornar `200` para todos os resultados.

---

# 23. Validação de dados

Todos os dados externos devem ser tratados como não confiáveis.

Validar:

* body;
* query parameters;
* path parameters;
* headers;
* token;
* variáveis de ambiente;
* dados retornados de integrações.

## Regras

* limitar tamanho de strings;
* remover espaços quando apropriado;
* não remover espaços internos válidos;
* não confiar no role enviado pelo cliente;
* não confiar no ID de usuário enviado pelo cliente;
* não confiar em preço ou estado enviados pelo frontend;
* não confiar que um ID existente continua válido;
* validar tipos com Pydantic;
* criar validators somente quando adicionarem valor claro.

Não espalhar validações iguais por múltiplos módulos.

---

# 24. Type hints

Toda função pública deve possuir tipos de entrada e saída.

Preferir:

```python
def get_user_by_email(
    session: Session,
    email: str,
) -> User | None: ...
```

Evitar:

```python
def get_user_by_email(session, email): ...
```

## Regras

* evitar `Any`;
* utilizar `Any` apenas quando a biblioteca realmente exigir;
* não utilizar `dict` genérico quando um schema ou tipo específico for melhor;
* não ignorar erros de tipagem sem justificativa;
* não adicionar casts apenas para silenciar o verificador;
* garantir que retornos opcionais sejam tratados.

---

# 25. Comentários e docstrings

Comentários devem explicar o motivo, não repetir o código.

Evitar:

```python
# Verifica se o usuário existe
if user is None:
    ...
```

Aceitável:

```python
# A resposta é intencionalmente genérica para evitar enumeração de usuários.
raise InvalidCredentialsError()
```

## Regras

* não comentar código óbvio;
* não deixar código comentado;
* não escrever textos extensos dentro de funções;
* utilizar docstrings em interfaces públicas ou comportamentos não óbvios;
* remover TODOs antes de concluir a tarefa;
* TODO só é aceitável quando acompanhado por uma issue ou limitação explicitamente solicitada.

---

# 26. Logging

Logs devem ajudar na investigação sem expor dados sensíveis.

Pode registrar:

* início da aplicação;
* ambiente utilizado;
* falhas inesperadas;
* IDs técnicos;
* falhas de integração;
* duração de operações importantes;
* resultado geral de migrations.

Não registrar:

* senha;
* hash de senha;
* JWT completo;
* segredo JWT;
* conteúdo do `.env`;
* dados pessoais sem necessidade;
* headers completos de autenticação.

Utilizar níveis corretamente:

* `DEBUG`: diagnóstico local;
* `INFO`: eventos normais importantes;
* `WARNING`: situação anormal recuperável;
* `ERROR`: falha em uma operação;
* `CRITICAL`: aplicação sem condição de continuar.

Não utilizar `print` em código de produção.

---

# 27. Testes obrigatórios

Nenhuma funcionalidade crítica está concluída sem testes.

## Cadastro

Testar:

* cadastro válido;
* normalização de e-mail;
* e-mail duplicado;
* senha e confirmação diferentes;
* senha inválida;
* campos obrigatórios;
* senha não retornada;
* hash não retornado;
* senha não armazenada em texto puro;
* papel padrão `STUDENT`.

## Login

Testar:

* login válido;
* e-mail inexistente;
* senha incorreta;
* normalização de e-mail;
* token retornado;
* token com expiração;
* resposta genérica para credenciais inválidas.

## Usuário atual

Testar:

* token válido;
* ausência de token;
* token inválido;
* token expirado;
* usuário inexistente;
* ausência de dados sensíveis na resposta.

## Inscrições

Testar:

* inscrição válida;
* usuário não autenticado;
* curso inexistente;
* inscrição duplicada;
* constraint única;
* usuário não consegue inscrever outra pessoa;
* transação revertida quando ocorre falha.

## Meus cursos

Testar:

* usuário sem cursos;
* usuário com um curso;
* usuário com vários cursos;
* usuário não recebe cursos de outra pessoa;
* rota sem autenticação;
* formato da resposta.

## Regras dos testes

* testes devem ser independentes;
* testes não devem depender de ordem;
* testes não devem acessar banco real;
* testes não devem acessar internet;
* testes não devem utilizar credenciais reais;
* utilizar fixtures pequenas;
* utilizar nomes que descrevam comportamento;
* testar resultados observáveis;
* evitar testar detalhes internos sem necessidade.

Exemplo de nome:

```python
def test_register_returns_conflict_when_email_already_exists(): ...
```

Evitar:

```python
def test_register_2(): ...
```

---

# 28. Organização dos testes

Utilizar Arrange, Act e Assert de maneira clara.

```python
def test_login_returns_token_for_valid_credentials(client, registered_user):
    # Arrange
    payload = {
        "email": registered_user.email,
        "password": "valid-password",
    }

    # Act
    response = client.post("/auth/login", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
```

Comentários de Arrange, Act e Assert são opcionais quando a separação já estiver visualmente clara.

Não criar um único teste que valide dez comportamentos diferentes.

---

# 29. Qualidade de código

Antes de considerar a tarefa concluída, executar:

```bash
ruff format --check .
ruff check .
pytest
```

Quando houver verificador de tipos configurado:

```bash
mypy app
```

ou:

```bash
pyright
```

Utilizar o verificador já adotado pelo projeto.

Não adicionar dois verificadores de tipos sem necessidade.

Se houver falha:

1. investigar a causa;
2. corrigir corretamente;
3. executar novamente;
4. não ignorar o erro;
5. não remover o teste;
6. não reduzir a validação apenas para fazer o pipeline passar.

---

# 30. Regras contra soluções frágeis

É proibido:

* utilizar `pass` em implementação final;
* utilizar retorno fixo para simular funcionalidade;
* colocar usuário autenticado manualmente;
* utilizar token estático;
* utilizar senha fixa;
* desabilitar autenticação para facilitar testes;
* capturar exceções e ignorá-las;
* utilizar `try/except` vazio;
* retornar listas falsas no código de produção;
* deixar mocks em produção;
* salvar token no banco sem necessidade;
* confiar no frontend para segurança;
* remover validações para contornar erro;
* adicionar sleeps para esconder problemas de concorrência;
* alterar testes corretos para acomodar código incorreto;
* utilizar dados reais em testes;
* expor configurações secretas no README;
* criar endpoints duplicados com nomes diferentes.

---

# 31. Performance adequada ao MVP

Não realizar otimizações prematuras.

Entretanto, evitar problemas evidentes:

* consultas N+1;
* carregar tabelas completas sem necessidade;
* executar múltiplas consultas idênticas na mesma operação;
* abrir sessões extras;
* fazer hash de senha repetidamente;
* consultar o usuário mais vezes do que o necessário;
* retornar colunas sensíveis ou não utilizadas;
* utilizar loops Python quando uma consulta simples resolve.

Paginação pode ser adicionada ao catálogo pelo responsável correspondente.

Para “Meus cursos”, manter a implementação simples e eficiente.

---

# 32. Compatibilidade com o frontend

O contrato da API deve ser previsível.

## Regras

* utilizar `snake_case` nos campos JSON;
* manter nomes de campos estáveis;
* não alterar resposta sem necessidade;
* informar erros com códigos consistentes;
* responder JSON;
* configurar CORS corretamente;
* aceitar `Authorization: Bearer <token>`;
* não exigir campos que o frontend não possui;
* não retornar estruturas diferentes dependendo do caminho interno;
* não expor models do banco diretamente.

Qualquer alteração de contrato deve considerar Lucas, responsável pelo frontend.

---

# 33. Contratos mínimos do MVP

## Cadastro

```http
POST /auth/register
```

## Login

```http
POST /auth/login
```

## Usuário atual

```http
GET /auth/me
Authorization: Bearer <token>
```

## Inscrição

```http
POST /courses/{course_id}/enroll
Authorization: Bearer <token>
```

## Cursos do usuário

```http
GET /users/me/courses
Authorization: Bearer <token>
```

Não criar endpoints adicionais para a mesma finalidade sem necessidade.

---

# 34. Documentação automática

Os endpoints devem aparecer corretamente no Swagger do FastAPI.

Cada rota deve declarar:

* schema de entrada;
* schema de saída;
* status de sucesso;
* possíveis respostas de erro importantes;
* tags coerentes;
* resumo curto.

Não escrever descrições enormes.

A documentação deve permitir que a equipe teste o fluxo sem analisar o código.

---

# 35. Ordem de prioridade

O agente deve respeitar esta ordem:

## P0 — obrigatório

1. aplicação inicializando;
2. conexão com banco funcionando;
3. cadastro;
4. login;
5. JWT;
6. `/auth/me`;
7. proteção de rotas;
8. inscrição em curso;
9. “Meus cursos”;
10. CORS;
11. testes;
12. integração com o módulo de cursos.

## P1 — somente após P0

* mensagens de erro mais detalhadas;
* logging aprimorado;
* cobertura adicional;
* documentação complementar;
* pequenos ajustes de performance.

## P2 — não implementar agora

* login com Google;
* refresh token;
* pagamento;
* gateway;
* e-mail;
* recuperação de senha;
* painel administrativo completo;
* arquitetura distribuída.

---

# 36. Fluxo obrigatório para demonstração

O backend precisa suportar, sem manipulação manual no banco:

```text
Criar usuário
→ fazer login
→ receber JWT
→ consultar usuário atual
→ listar cursos
→ abrir um curso
→ inscrever usuário
→ consultar cursos do usuário
→ acessar conteúdo permitido
```

Arthur é responsável por garantir que autenticação e inscrição funcionem nesse fluxo.

---

# 37. Processo de trabalho do agente

Para cada tarefa, o agente deve seguir:

## 1. Investigar

* verificar arquivos existentes;
* localizar implementações relacionadas;
* localizar testes;
* entender contratos.

## 2. Definir a alteração

* identificar arquivos necessários;
* evitar alterações fora do escopo;
* preservar compatibilidade.

## 3. Implementar

* escrever código simples;
* manter separação de responsabilidades;
* adicionar validações;
* tratar erros;
* adicionar tipos.

## 4. Testar

* criar ou atualizar testes;
* executar testes relacionados;
* executar suíte completa;
* executar lint;
* executar formatação;
* executar tipagem quando configurada.

## 5. Revisar

Antes de concluir, verificar:

* há código duplicado?
* há segredo exposto?
* há erro silencioso?
* há função com muitas responsabilidades?
* há dependência circular?
* há campo sensível na resposta?
* há rota sem proteção?
* há consulta sem tratamento?
* há teste ausente?
* o contrato do frontend foi preservado?

## 6. Relatar

Ao finalizar, informar objetivamente:

* arquivos criados;
* arquivos alterados;
* funcionalidades implementadas;
* testes executados;
* resultado dos comandos;
* decisões importantes;
* limitações reais restantes.

Não afirmar que testes passaram sem executá-los.

---

# 38. Regra de alteração mínima

Não alterar arquivos não relacionados apenas para:

* renomear coisas;
* aplicar preferência pessoal;
* reorganizar imports de todo o projeto;
* substituir arquitetura;
* trocar biblioteca;
* reformular módulos estáveis;
* aumentar artificialmente o escopo.

Mudanças maiores precisam possuir motivo técnico ligado à tarefa.

---

# 39. Regra de dependências

Antes de adicionar uma dependência:

1. verificar se o projeto já possui solução equivalente;
2. verificar se a biblioteca é realmente necessária;
3. preferir bibliotecas mantidas;
4. evitar pacotes que executem funções simples já cobertas pela linguagem;
5. registrar a dependência no arquivo correto;
6. não instalar dependências globais;
7. não importar uma biblioteca sem adicioná-la ao projeto.

Não escolher uma biblioteca apenas porque ela reduz uma função de cinco linhas para uma linha.

Para criptografia, JWT e hash de senha, utilizar bibliotecas confiáveis em vez de implementação própria.

---

# 40. Regra de segurança

Toda mudança relacionada a autenticação deve ser revisada considerando:

* armazenamento de senha;
* criação do token;
* validação do token;
* expiração;
* autorização;
* exposição de dados;
* enumeração de usuários;
* logs;
* configurações;
* manipulação de identidade;
* acesso entre usuários.

O frontend nunca é uma fronteira de segurança.

Ocultar um botão não substitui uma validação no backend.

---

# 41. Definition of Done

Uma tarefa só está concluída quando:

* o requisito foi implementado;
* o código possui tipos;
* o código segue a arquitetura do projeto;
* as responsabilidades estão separadas;
* não existem segredos no código;
* entradas são validadas;
* erros esperados são tratados;
* respostas não expõem dados sensíveis;
* testes foram adicionados ou atualizados;
* testes relacionados passaram;
* suíte completa passou;
* lint passou;
* formatação passou;
* documentação da API está correta;
* contrato do frontend foi preservado;
* não existem mocks ou retornos temporários em produção;
* não existem TODOs não justificados;
* a aplicação inicializa;
* o fluxo principal foi testado.

---

# 42. Checklist final obrigatório

Antes de encerrar qualquer implementação, confirmar:

```text
[ ] A aplicação inicia sem erro.
[ ] As configurações vêm do ambiente.
[ ] Nenhum segredo foi versionado.
[ ] O cadastro funciona.
[ ] E-mail duplicado é tratado.
[ ] A senha é armazenada somente como hash.
[ ] A senha não aparece na resposta.
[ ] O login válido retorna JWT.
[ ] O login inválido retorna erro genérico.
[ ] O JWT expira.
[ ] Tokens inválidos são rejeitados.
[ ] /auth/me exige autenticação.
[ ] A inscrição exige autenticação.
[ ] O curso precisa existir.
[ ] Inscrição duplicada é impedida.
[ ] A duplicidade também é impedida no banco.
[ ] O usuário não consegue agir em nome de outro usuário.
[ ] “Meus cursos” retorna somente dados do usuário atual.
[ ] O CORS permite o frontend correto.
[ ] Os erros seguem um padrão.
[ ] Os endpoints aparecem no Swagger.
[ ] Os testes não usam banco de produção.
[ ] Os testes passam.
[ ] O Ruff passa.
[ ] O verificador de tipos passa, quando configurado.
[ ] Não há código temporário em produção.
```

---

# 43. Diretriz final

O objetivo não é produzir o maior código possível.

O objetivo é produzir a menor implementação que seja:

* correta;
* segura;
* clara;
* testada;
* previsível;
* integrada;
* sustentável.

Código inteligente demais costuma ser difícil de manter.

Prefira código explícito, nomes claros, dependências controladas, regras centralizadas e testes que representem o comportamento real do sistema.
