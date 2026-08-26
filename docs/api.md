# Contrato HTTP do MVP

Todas as respostas são JSON. Sucessos usam `{"data": ...}` (exceto o health
check) e falhas usam:

```json
{
  "error": {
    "code": "STABLE_ERROR_CODE",
    "message": "Mensagem legível.",
    "details": null
  }
}
```

## Autenticação

### `POST /api/auth/register`

Não exige autenticação. Body:

```json
{
  "name": "Arthur",
  "email": "arthur@example.com",
  "password": "uma-senha-segura",
  "password_confirmation": "uma-senha-segura"
}
```

Retorna `201` com `id`, `name`, `email`, `role` e `created_at`. Erros principais:
`422 VALIDATION_ERROR` e `409 EMAIL_ALREADY_REGISTERED`.

### `POST /api/auth/login`

Não exige autenticação. Body:

```json
{
  "email": "arthur@example.com",
  "password": "uma-senha-segura"
}
```

Retorna `200` com `access_token` e `token_type: "bearer"`. Credenciais inválidas
retornam `401 INVALID_CREDENTIALS` sem informar qual campo está incorreto.

### `GET /api/auth/me`

Exige `Authorization: Bearer <token>`. Retorna `200` com os dados públicos do
usuário. Pode retornar `401 AUTHENTICATION_REQUIRED`, `401 INVALID_TOKEN`,
`401 TOKEN_EXPIRED` ou `404 USER_NOT_FOUND`.

## Inscrições

### `POST /api/courses/<course_id>/enroll`

Exige Bearer token e não aceita a escolha de `user_id`; a identidade sempre vem
do JWT. Retorna `201` com `id`, `user_id`, `course_id` e `created_at`. Pode
retornar `404 COURSE_NOT_FOUND` ou `409 ALREADY_ENROLLED`.

### `GET /api/users/me/courses`

Exige Bearer token. Retorna `200` e uma lista de cursos, vazia quando o usuário
não possui inscrições. Cada curso contém `id`, `title`, `description`,
`thumbnail_url` e `level`.

Os endpoints de inscrição dependem da tabela real `courses` do módulo de
catálogo. Enquanto ela não existir ou não cumprir o contrato público acima, a
API retorna `503 COURSE_INTEGRATION_UNAVAILABLE`.

## Operação

### `GET /api/health`

Não exige autenticação. Retorna `200`:

```json
{"status": "ok"}
```

