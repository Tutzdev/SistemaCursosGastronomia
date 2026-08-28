def test_homepage_renders_course_experience(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert b"Cursos" in response.data
    assert b"course-grid" in response.data
    assert b"newsletter-form" in response.data
    assert b"Depoimentos" not in response.data


def test_frontend_assets_are_available(client) -> None:
    for path in (
        "/static/css/styles.css",
        "/static/js/app.js",
        "/static/images/hero-gastronomia.png",
        "/static/images/chef-banner.png",
    ):
        assert client.get(path).status_code == 200


def test_site_pages_are_available(client) -> None:
    expected_content = {
        "/cursos": b"Todos os cursos",
        "/sobre": b"Uma escola criada",
        "/contato": b"Vamos conversar",
        "/cursos/pizza-napolitana": b"Pizza Napolitana",
    }

    for path, content in expected_content.items():
        response = client.get(path)
        assert response.status_code == 200
        assert content in response.data


def test_unknown_course_page_returns_not_found(client) -> None:
    assert client.get("/cursos/curso-inexistente").status_code == 404
