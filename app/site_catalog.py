from collections.abc import Mapping

SITE_COURSES: tuple[dict[str, object], ...] = (
    {
        "slug": "pizza-napolitana",
        "title": "Pizza Napolitana",
        "category": "Pizzas",
        "image": "images/course-pizza.jpg",
        "badge": "Mais vendido",
        "price": "R$ 189,00",
        "level": "Iniciante",
        "duration": "8 horas",
        "lessons": 24,
        "rating": "4,9",
        "reviews": 486,
        "description": (
            "Da fermentação lenta ao forno: domine uma massa leve, borda "
            "aerada e coberturas equilibradas."
        ),
        "tagline": "A autêntica pizza napolitana, adaptada à sua cozinha.",
        "instructor": "Chef Lorenzo Bianchi",
        "instructor_role": "Pizzaiolo e pesquisador de fermentação",
        "instructor_bio": (
            "Lorenzo trabalha há 18 anos com massas de longa fermentação e "
            "formou mais de 4 mil alunos entre cozinhas caseiras e profissionais."
        ),
        "learnings": (
            "Preparar massas com fermentação de 24 e 48 horas",
            "Reconhecer o ponto ideal de glúten e fermentação",
            "Fazer molho italiano sem cocção e coberturas equilibradas",
            "Assar com excelente resultado em um forno doméstico",
        ),
        "modules": (
            (
                "Fundamentos da massa",
                (
                    "Ingredientes e proporções",
                    "Sova e dobras",
                    "Fermentação controlada",
                ),
            ),
            (
                "Molhos e coberturas",
                ("Molho napolitano", "Queijos e umidade", "Combinações clássicas"),
            ),
            (
                "Abertura e forno",
                ("Abertura sem rolo", "Montagem", "Cocção e finalização"),
            ),
        ),
    },
    {
        "slug": "panificacao-artesanal",
        "title": "Panificação Artesanal",
        "category": "Panificação",
        "image": "images/course-bread.jpg",
        "badge": "Novo",
        "price": "R$ 169,00",
        "level": "Iniciante",
        "duration": "10 horas",
        "lessons": 28,
        "rating": "4,8",
        "reviews": 312,
        "description": (
            "Aprenda levain, fermentação e modelagem para criar pães de casca "
            "crocante e miolo perfeito."
        ),
        "tagline": "Pão de verdade, feito com tempo e poucos ingredientes.",
        "instructor": "Chef Helena Duarte",
        "instructor_role": "Padeira e especialista em fermentação natural",
        "instructor_bio": (
            "Helena comanda uma padaria artesanal há 12 anos e ensina processos "
            "precisos, possíveis e adaptados à rotina de casa."
        ),
        "learnings": (
            "Criar e manter um fermento natural saudável",
            "Trabalhar hidratação, dobras e desenvolvimento de glúten",
            "Modelar pães redondos, alongados e recheados",
            "Controlar vapor, temperatura e ponto de cocção",
        ),
        "modules": (
            (
                "Começando o levain",
                ("Fermento natural", "Alimentação", "Diagnóstico do levain"),
            ),
            ("Construção da massa", ("Autólise", "Dobras", "Fermentação em bloco")),
            ("Modelagem e cocção", ("Pré-modelagem", "Cortes", "Forno com vapor")),
        ),
    },
    {
        "slug": "confeitaria-essencial",
        "title": "Confeitaria Essencial",
        "category": "Confeitaria",
        "image": "images/course-confeitaria.jpg",
        "badge": "Favorito",
        "price": "R$ 159,00",
        "level": "Iniciante",
        "duration": "9 horas",
        "lessons": 26,
        "rating": "4,9",
        "reviews": 274,
        "description": (
            "Bases, cremes e massas clássicas explicadas com precisão para "
            "sobremesas sempre consistentes."
        ),
        "tagline": "Técnica e delicadeza para sobremesas inesquecíveis.",
        "instructor": "Chef Clara Fontes",
        "instructor_role": "Confeiteira e consultora de pâtisserie",
        "instructor_bio": (
            "Clara transforma técnicas clássicas em processos claros, com foco "
            "em textura, equilíbrio de sabores e acabamento elegante."
        ),
        "learnings": (
            "Dominar massas aeradas, quebradiças e cremosas",
            "Preparar cremes, ganaches e pontos de calda",
            "Combinar texturas e sabores sem excesso de açúcar",
            "Montar, finalizar e conservar sobremesas",
        ),
        "modules": (
            (
                "Bases da confeitaria",
                ("Pesos e temperaturas", "Massas essenciais", "Caldas"),
            ),
            ("Cremes e recheios", ("Creme confeiteiro", "Ganaches", "Emulsões")),
            ("Montagem", ("Camadas", "Acabamentos", "Conservação")),
        ),
    },
    {
        "slug": "bolos-decorados",
        "title": "Bolos Decorados",
        "category": "Confeitaria",
        "image": "images/course-bolos.jpg",
        "badge": "Lançamento",
        "price": "R$ 179,00",
        "level": "Intermediário",
        "duration": "12 horas",
        "lessons": 32,
        "rating": "4,8",
        "reviews": 198,
        "description": (
            "Estrutura, recheios e acabamentos modernos para bolos elegantes, "
            "firmes e cheios de sabor."
        ),
        "tagline": "Bolos que impressionam antes mesmo da primeira fatia.",
        "instructor": "Chef Marcela Rocha",
        "instructor_role": "Cake designer e confeiteira",
        "instructor_bio": (
            "Marcela é especialista em bolos de celebração e desenvolveu um "
            "método que combina estabilidade, acabamento e sabor."
        ),
        "learnings": (
            "Nivelar, rechear e prensar bolos altos",
            "Construir estruturas seguras para diferentes tamanhos",
            "Aplicar buttercream liso e técnicas com bico",
            "Criar paletas e decorações com identidade",
        ),
        "modules": (
            ("Estrutura", ("Massas estáveis", "Recheios", "Prensagem")),
            ("Cobertura", ("Buttercream", "Alisamento", "Quinas perfeitas")),
            ("Decoração", ("Bicos", "Texturas", "Composição final")),
        ),
    },
    {
        "slug": "massas-frescas",
        "title": "Massas Frescas",
        "category": "Massas",
        "image": "images/course-massas.jpg",
        "badge": "Mais vendido",
        "price": "R$ 197,00",
        "level": "Iniciante",
        "duration": "7 horas",
        "lessons": 21,
        "rating": "4,9",
        "reviews": 641,
        "description": (
            "Prepare massas do zero e transforme poucos ingredientes em "
            "tagliatelle, ravioli e muito mais."
        ),
        "tagline": "Farinha, ovos e técnica: a Itália na sua mesa.",
        "instructor": "Chef Enzo Bellini",
        "instructor_role": "Especialista em cozinha italiana regional",
        "instructor_bio": (
            "Enzo cresceu entre cozinhas familiares e restaurantes na Emilia-"
            "Romagna. Hoje ensina a tradição de forma prática e sem mistério."
        ),
        "learnings": (
            "Escolher farinhas e acertar proporções da massa",
            "Sovar, descansar e abrir à mão ou no cilindro",
            "Produzir tagliatelle, ravioli e massas recheadas",
            "Preparar cinco molhos essenciais",
        ),
        "modules": (
            ("A massa perfeita", ("Farinhas", "Proporções", "Sova e descanso")),
            ("Formatos", ("Tagliatelle", "Pappardelle", "Ravioli")),
            ("Molhos", ("Manteiga e sálvia", "Pomodoro", "Ragù")),
        ),
    },
    {
        "slug": "cozinha-profissional",
        "title": "Cozinha Profissional",
        "category": "Cozinha",
        "image": "images/course-cozinha.jpg",
        "badge": "Formação",
        "price": "R$ 239,00",
        "level": "Intermediário",
        "duration": "16 horas",
        "lessons": 40,
        "rating": "4,9",
        "reviews": 356,
        "description": (
            "Organização, cortes, cocções e montagem para levar técnica "
            "profissional à sua cozinha."
        ),
        "tagline": "Método, precisão e criatividade em cada serviço.",
        "instructor": "Chef Rafael Lemos",
        "instructor_role": "Chef executivo e professor de gastronomia",
        "instructor_bio": (
            "Rafael reúne duas décadas de restaurantes e sala de aula em uma "
            "formação completa para quem quer cozinhar com método."
        ),
        "learnings": (
            "Organizar mise en place e fluxo de produção",
            "Executar cortes clássicos com precisão e segurança",
            "Aplicar métodos de cocção para cada ingrediente",
            "Criar fundos, molhos e montagens equilibradas",
        ),
        "modules": (
            ("Organização", ("Mise en place", "Segurança", "Fluxo de trabalho")),
            ("Técnicas", ("Cortes", "Cocções", "Fundos e molhos")),
            ("Serviço", ("Planejamento", "Montagem", "Finalização")),
        ),
    },
)


def get_site_course(slug: str) -> Mapping[str, object] | None:
    return next((course for course in SITE_COURSES if course["slug"] == slug), None)
