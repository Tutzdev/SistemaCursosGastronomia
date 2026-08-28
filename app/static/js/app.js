const COURSE_CATALOG = [
  {
    id: "pizza-napolitana",
    title: "Pizza Napolitana",
    category: "Pizzas",
    categorySlug: "pizzas",
    description: "Da fermentação lenta ao forno: domine uma massa leve, borda aerada e coberturas equilibradas.",
    image: "/static/images/course-pizza.jpg",
    level: "Iniciante",
    duration: "8 horas",
    lessons: 24,
    price: 189,
    rating: "4,9",
    reviews: 486,
    badge: "Mais vendido",
    badgeTone: "green",
    learnings: ["Massa com fermentação de 24 e 48 horas", "Molho de tomate italiano sem cocção", "Modelagem, abertura e cocção em forno doméstico"],
  },
  {
    id: "panificacao-artesanal",
    title: "Panificação Artesanal",
    category: "Panificação",
    categorySlug: "panificacao",
    description: "Aprenda levain, fermentação e modelagem para criar pães de casca crocante e miolo perfeito.",
    image: "/static/images/course-bread.jpg",
    level: "Iniciante",
    duration: "10 horas",
    lessons: 28,
    price: 169,
    rating: "4,8",
    reviews: 312,
    badge: "Novo",
    badgeTone: "red",
    learnings: ["Criação e manutenção de fermento natural", "Dobras, hidratação e desenvolvimento de glúten", "Ponto de fermentação, cortes e cocção com vapor"],
  },
  {
    id: "confeitaria-essencial",
    title: "Confeitaria Essencial",
    category: "Confeitaria",
    categorySlug: "confeitaria",
    description: "Bases, cremes e massas clássicas explicadas com precisão para sobremesas sempre consistentes.",
    image: "/static/images/course-confeitaria.jpg",
    level: "Iniciante",
    duration: "9 horas",
    lessons: 26,
    price: 159,
    rating: "4,9",
    reviews: 274,
    badge: "Favorito",
    badgeTone: "green",
    learnings: ["Massas básicas e controle de temperatura", "Cremes, ganaches e pontos de calda", "Montagem, finalização e conservação"],
  },
  {
    id: "bolos-decorados",
    title: "Bolos Decorados",
    category: "Confeitaria",
    categorySlug: "confeitaria",
    description: "Estrutura, recheios e acabamentos modernos para bolos elegantes, firmes e cheios de sabor.",
    image: "/static/images/course-bolos.jpg",
    level: "Intermediário",
    duration: "12 horas",
    lessons: 32,
    price: 179,
    rating: "4,8",
    reviews: 198,
    badge: "Lançamento",
    badgeTone: "red",
    learnings: ["Nivelamento, prensagem e estruturação", "Buttercream liso e técnicas com bico", "Composição de sabores e decoração autoral"],
  },
  {
    id: "massas-frescas",
    title: "Massas Frescas",
    category: "Massas",
    categorySlug: "massas",
    description: "Prepare massas do zero e transforme poucos ingredientes em tagliatelle, ravioli e muito mais.",
    image: "/static/images/course-massas.jpg",
    level: "Iniciante",
    duration: "7 horas",
    lessons: 21,
    price: 197,
    rating: "4,9",
    reviews: 641,
    badge: "Mais vendido",
    badgeTone: "green",
    learnings: ["Proporções, sova e descanso da massa", "Abertura manual e com cilindro", "Cortes, recheios e cinco molhos essenciais"],
  },
  {
    id: "cozinha-profissional",
    title: "Cozinha Profissional",
    category: "Cozinha",
    categorySlug: "cozinha",
    description: "Organização, cortes, cocções e montagem para levar técnica profissional à sua cozinha.",
    image: "/static/images/course-cozinha.jpg",
    level: "Intermediário",
    duration: "16 horas",
    lessons: 40,
    price: 239,
    rating: "4,9",
    reviews: 356,
    badge: "Formação",
    badgeTone: "red",
    learnings: ["Mise en place e fluxo de cozinha", "Cortes clássicos e métodos de cocção", "Fundos, molhos e montagem de pratos"],
  },
];

const state = {
  courses: [...COURSE_CATALOG],
  query: "",
  category: "all",
  level: "all",
  cart: loadCart(),
  activeModalCourse: null,
};

const elements = {
  courseGrid: document.querySelector("#course-grid"),
  emptyState: document.querySelector("#empty-state"),
  categoryList: document.querySelector("#category-list"),
  searchForm: document.querySelector("#search-form"),
  searchInput: document.querySelector("#course-search"),
  activeFilter: document.querySelector("#active-filter"),
  activeFilterLabel: document.querySelector("#active-filter-label"),
  cartDrawer: document.querySelector("#cart-drawer"),
  cartBackdrop: document.querySelector("#drawer-backdrop"),
  cartItems: document.querySelector("#cart-items"),
  cartEmpty: document.querySelector("#cart-empty"),
  cartSummary: document.querySelector("#cart-summary"),
  cartCount: document.querySelector("#cart-count"),
  cartTotal: document.querySelector("#cart-total"),
  courseModal: document.querySelector("#course-modal"),
  menuButton: document.querySelector("#menu-button"),
  mobileNav: document.querySelector("#mobile-nav"),
  toast: document.querySelector("#toast"),
};

function loadCart() {
  try {
    const saved = JSON.parse(localStorage.getItem("cursos-cart"));
    return Array.isArray(saved) ? saved.map(String) : [];
  } catch {
    return [];
  }
}

function persistCart() {
  try {
    localStorage.setItem("cursos-cart", JSON.stringify(state.cart));
  } catch {
    // A interface continua funcionando mesmo quando o navegador bloqueia storage.
  }
}

function normalize(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2,
  }).format(value);
}

function filteredCourses() {
  const query = normalize(state.query);
  return state.courses.filter((course) => {
    const inCategory = state.category === "all" || course.categorySlug === state.category;
    const inLevel = state.level === "all" || normalize(course.level) === state.level;
    const searchable = normalize(`${course.title} ${course.category} ${course.description} ${course.level}`);
    return inCategory && inLevel && (!query || searchable.includes(query));
  });
}

function courseCard(course) {
  const id = escapeHtml(course.id);
  return `
    <article class="course-card">
      <div class="course-media">
        <img src="${escapeHtml(course.image)}" alt="${escapeHtml(course.title)}" loading="lazy">
        <span class="course-badge ${course.badgeTone === "red" ? "red" : ""}">${escapeHtml(course.badge)}</span>
      </div>
      <div class="course-body">
        <span class="course-category">${escapeHtml(course.category)}</span>
        <a class="course-title-button" href="/cursos/${encodeURIComponent(course.id)}">
          <h3>${escapeHtml(course.title)}</h3>
        </a>
        <p class="course-description">${escapeHtml(course.description)}</p>
        <div class="course-meta">
          <span class="course-rating"><b aria-hidden="true">★</b> ${escapeHtml(course.rating)} (${course.reviews})</span>
          <span>${escapeHtml(course.duration)}</span>
          <span>${course.lessons} aulas</span>
        </div>
        <div class="course-footer">
          <span class="course-price"><small>por apenas</small>${formatCurrency(course.price)}</span>
          <div class="card-actions">
            <a class="details-button" href="/cursos/${encodeURIComponent(course.id)}">Detalhes</a>
            <button class="add-cart-button" type="button" data-action="add" data-course-id="${id}" aria-label="Adicionar ${escapeHtml(course.title)} ao carrinho">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2 12h10.5l2-8H6"/><circle cx="9" cy="20" r="1"/><circle cx="17" cy="20" r="1"/></svg>
            </button>
          </div>
        </div>
      </div>
    </article>`;
}

function renderCourses() {
  if (!elements.courseGrid) return;
  const courses = filteredCourses();
  elements.courseGrid.innerHTML = courses.map(courseCard).join("");
  elements.emptyState.hidden = courses.length > 0;

  const filters = [];
  if (state.category !== "all") {
    const selected = state.courses.find((course) => course.categorySlug === state.category);
    filters.push(`Categoria: ${selected?.category ?? state.category}`);
  }
  if (state.level !== "all") filters.push(`Nível: ${state.level}`);
  if (state.query) filters.push(`Busca: “${state.query}”`);
  if (elements.activeFilter) elements.activeFilter.hidden = filters.length === 0;
  if (elements.activeFilterLabel) elements.activeFilterLabel.textContent = filters.join(" • ");
  const resultCount = document.querySelector("#catalog-result-count");
  if (resultCount) {
    resultCount.textContent = `${courses.length} ${courses.length === 1 ? "curso encontrado" : "cursos encontrados"}`;
  }
  syncCategoryButtons();
}

function renderCategories() {
  if (!elements.categoryList) return;
  const categories = [...new Map(state.courses.map((course) => [course.categorySlug, {
    slug: course.categorySlug,
    name: course.category,
    image: course.image,
  }])).values()];

  const allButton = `
    <button class="category-button active" type="button" role="tab" aria-selected="true" data-category="all">
      <span class="category-count">${state.courses.length}</span>
      <img src="/static/images/hero-gastronomia.png" alt="" loading="lazy">
      <span>Todos</span>
    </button>`;

  elements.categoryList.innerHTML = allButton + categories.map((category) => {
    const count = state.courses.filter((course) => course.categorySlug === category.slug).length;
    return `
      <button class="category-button" type="button" role="tab" aria-selected="false" data-category="${escapeHtml(category.slug)}">
        <span class="category-count">${count}</span>
        <img src="${escapeHtml(category.image)}" alt="" loading="lazy">
        <span>${escapeHtml(category.name)}</span>
      </button>`;
  }).join("");
}

function syncCategoryButtons() {
  document.querySelectorAll("[data-category]").forEach((button) => {
    const active = button.dataset.category === state.category;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
  });
}

function resetFilters({ scroll = true } = {}) {
  state.query = "";
  state.category = "all";
  state.level = "all";
  elements.searchInput.value = "";
  const catalogSearchInput = document.querySelector("#catalog-search-input");
  const levelFilter = document.querySelector("#level-filter");
  if (catalogSearchInput) catalogSearchInput.value = "";
  if (levelFilter) levelFilter.value = "all";
  renderCourses();
  const courseSection = document.querySelector("#cursos") ?? document.querySelector(".catalog-page-section");
  if (scroll && courseSection) courseSection.scrollIntoView({ behavior: "smooth" });
}

function findCourse(id) {
  return state.courses.find((course) => String(course.id) === String(id));
}

function renderCart() {
  state.cart = state.cart.filter((id) => findCourse(id));
  const courses = state.cart.map(findCourse).filter(Boolean);
  elements.cartCount.textContent = courses.length;
  elements.cartCount.setAttribute("aria-label", `${courses.length} ${courses.length === 1 ? "item" : "itens"}`);
  elements.cartEmpty.hidden = courses.length > 0;
  elements.cartSummary.hidden = courses.length === 0;
  elements.cartItems.hidden = courses.length === 0;
  elements.cartItems.innerHTML = courses.map((course) => `
    <article class="cart-item">
      <img src="${escapeHtml(course.image)}" alt="">
      <div><h3>${escapeHtml(course.title)}</h3><strong>${formatCurrency(course.price)}</strong></div>
      <button class="remove-cart-item" type="button" data-remove-id="${escapeHtml(course.id)}" aria-label="Remover ${escapeHtml(course.title)}">×</button>
    </article>`).join("");
  elements.cartTotal.textContent = formatCurrency(courses.reduce((total, course) => total + course.price, 0));
  persistCart();
}

function addToCart(id) {
  const course = findCourse(id);
  if (!course) return;
  if (state.cart.includes(String(course.id))) {
    showToast(`${course.title} já está no seu carrinho.`);
    openCart();
    return;
  }
  state.cart.push(String(course.id));
  renderCart();
  showToast(`${course.title} foi adicionado ao carrinho.`);
}

function removeFromCart(id) {
  const course = findCourse(id);
  state.cart = state.cart.filter((itemId) => itemId !== String(id));
  renderCart();
  showToast(`${course?.title ?? "Curso"} foi removido.`);
}

function openCart() {
  closeModal();
  elements.cartBackdrop.hidden = false;
  elements.cartDrawer.setAttribute("aria-hidden", "false");
  document.querySelector(".cart-trigger").setAttribute("aria-expanded", "true");
  document.body.classList.add("locked");
  requestAnimationFrame(() => elements.cartDrawer.classList.add("open"));
  window.setTimeout(() => document.querySelector("#close-cart").focus(), 100);
}

function closeCart() {
  elements.cartDrawer.classList.remove("open");
  elements.cartDrawer.setAttribute("aria-hidden", "true");
  document.querySelector(".cart-trigger").setAttribute("aria-expanded", "false");
  document.body.classList.remove("locked");
  window.setTimeout(() => { elements.cartBackdrop.hidden = true; }, 320);
}

function openModal(id) {
  const course = findCourse(id);
  if (!course) return;
  state.activeModalCourse = String(course.id);
  document.querySelector("#modal-image").src = course.image;
  document.querySelector("#modal-image").alt = course.title;
  document.querySelector("#modal-category").textContent = course.category;
  document.querySelector("#modal-level").textContent = course.level;
  document.querySelector("#modal-title").textContent = course.title;
  document.querySelector("#modal-description").textContent = course.description;
  document.querySelector("#modal-duration").textContent = course.duration;
  document.querySelector("#modal-lessons").textContent = String(course.lessons);
  document.querySelector("#modal-price").textContent = formatCurrency(course.price);
  document.querySelector("#modal-learnings").innerHTML = course.learnings.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  elements.courseModal.hidden = false;
  document.body.classList.add("locked");
  window.setTimeout(() => document.querySelector(".modal-close").focus(), 50);
}

function closeModal() {
  if (elements.courseModal.hidden) return;
  elements.courseModal.hidden = true;
  state.activeModalCourse = null;
  document.body.classList.remove("locked");
}

let toastTimer;
function showToast(message) {
  window.clearTimeout(toastTimer);
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  toastTimer = window.setTimeout(() => elements.toast.classList.remove("show"), 3200);
}

function setCategory(category) {
  state.category = category;
  renderCourses();
  const courseSection = document.querySelector("#cursos") ?? document.querySelector(".catalog-page-section");
  courseSection?.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadApiCourses() {
  try {
    const response = await fetch("/api/courses", { headers: { Accept: "application/json" } });
    if (!response.ok) return;
    const payload = await response.json();
    if (!Array.isArray(payload.data) || payload.data.length === 0) return;

    state.courses = COURSE_CATALOG.map((local) => {
      const apiCourse = payload.data.find((course) => normalize(course.title) === normalize(local.title));
      if (!apiCourse) return local;
      return {
        ...local,
        apiId: String(apiCourse.id),
        title: apiCourse.title,
        category: apiCourse.category?.name ?? local.category,
        categorySlug: apiCourse.category?.slug ?? local.categorySlug,
        description: apiCourse.description?.startsWith("Curso demonstrativo") ? local.description : (apiCourse.description ?? local.description),
        level: apiCourse.level === "INTERMEDIATE" ? "Intermediário" : apiCourse.level === "ADVANCED" ? "Avançado" : "Iniciante",
      };
    });
    renderCategories();
    renderCourses();
    renderCart();
  } catch {
    // O catálogo editorial local mantém a home útil sem banco configurado.
  }
}

elements.courseGrid?.addEventListener("click", (event) => {
  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) return;
  const { action, courseId } = actionButton.dataset;
  if (action === "details") openModal(courseId);
  if (action === "add") addToCart(courseId);
});

elements.categoryList?.addEventListener("click", (event) => {
  const categoryButton = event.target.closest("[data-category]");
  if (!categoryButton) return;
  if (document.body.dataset.page === "index") {
    window.location.href = `/cursos?category=${encodeURIComponent(categoryButton.dataset.category)}`;
    return;
  }
  setCategory(categoryButton.dataset.category);
});

elements.searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = elements.searchInput.value.trim();
  if (!elements.courseGrid) {
    window.location.href = `/cursos?q=${encodeURIComponent(query)}`;
    return;
  }
  state.query = query;
  const catalogSearchInput = document.querySelector("#catalog-search-input");
  if (catalogSearchInput) catalogSearchInput.value = query;
  renderCourses();
  const courseSection = document.querySelector("#cursos") ?? document.querySelector(".catalog-page-section");
  courseSection?.scrollIntoView({ behavior: "smooth" });
});

let searchTimer;
elements.searchInput.addEventListener("input", () => {
  if (!elements.courseGrid) return;
  window.clearTimeout(searchTimer);
  searchTimer = window.setTimeout(() => {
    state.query = elements.searchInput.value.trim();
    renderCourses();
  }, 180);
});

document.querySelectorAll(".scroll-to-courses").forEach((button) => {
  button.addEventListener("click", () => {
    window.location.href = "/cursos";
  });
});

document.querySelector("#show-all-courses")?.addEventListener("click", () => {
  window.location.href = "/cursos";
});
document.querySelector("#show-all-categories")?.addEventListener("click", () => resetFilters());
document.querySelector("#clear-filter")?.addEventListener("click", () => resetFilters({ scroll: false }));
document.querySelector(".contact-trigger")?.addEventListener("click", () => {
  window.location.href = "/sobre";
});
document.querySelector(".back-to-top").addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

document.querySelector(".cart-trigger").addEventListener("click", openCart);
document.querySelector("#close-cart").addEventListener("click", closeCart);
elements.cartBackdrop.addEventListener("click", closeCart);
document.querySelector("#browse-courses").addEventListener("click", () => {
  closeCart();
  const homeCourses = document.querySelector("#cursos");
  if (homeCourses) {
    window.setTimeout(() => homeCourses.scrollIntoView({ behavior: "smooth" }), 260);
  } else {
    window.location.href = "/cursos";
  }
});

elements.cartItems.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-id]");
  if (removeButton) removeFromCart(removeButton.dataset.removeId);
});

document.querySelector("#checkout-button").addEventListener("click", () => {
  showToast("Sua seleção está pronta. Entre na sua conta para concluir a inscrição.");
});

document.querySelector(".modal-close").addEventListener("click", closeModal);
elements.courseModal.addEventListener("click", (event) => {
  if (event.target === elements.courseModal) closeModal();
});
document.querySelector("#modal-add-cart").addEventListener("click", () => {
  if (!state.activeModalCourse) return;
  const courseId = state.activeModalCourse;
  closeModal();
  addToCart(courseId);
  openCart();
});

elements.menuButton.addEventListener("click", () => {
  const open = elements.mobileNav.hidden;
  elements.mobileNav.hidden = !open;
  elements.menuButton.classList.toggle("open", open);
  elements.menuButton.setAttribute("aria-expanded", String(open));
  elements.menuButton.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
});

elements.mobileNav.addEventListener("click", (event) => {
  if (!event.target.closest("a")) return;
  elements.mobileNav.hidden = true;
  elements.menuButton.classList.remove("open");
  elements.menuButton.setAttribute("aria-expanded", "false");
});

document.querySelector("#newsletter-form")?.addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.querySelector("#newsletter-email");
  showToast(`Pronto! Novidades serão enviadas para ${input.value}.`);
  event.currentTarget.reset();
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  closeModal();
  closeCart();
  if (!elements.mobileNav.hidden) elements.menuButton.click();
});

document.querySelectorAll("[data-course-add]").forEach((button) => {
  button.addEventListener("click", () => {
    addToCart(button.dataset.courseAdd);
    openCart();
  });
});

document.querySelectorAll("[data-tab]").forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.dataset.tab;
    document.querySelectorAll("[data-tab]").forEach((item) => {
      const active = item === tab;
      item.classList.toggle("active", active);
      item.setAttribute("aria-selected", String(active));
    });
    document.querySelectorAll("[data-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.panel !== target;
    });
  });
});

document.querySelectorAll("[data-module-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    const lessons = button.nextElementSibling;
    const open = lessons.hidden;
    lessons.hidden = !open;
    button.setAttribute("aria-expanded", String(open));
    button.closest(".module-item").classList.toggle("open", open);
  });
});

document.querySelectorAll("[data-faq-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    const answer = button.nextElementSibling;
    const open = answer.hidden;
    answer.hidden = !open;
    button.setAttribute("aria-expanded", String(open));
    button.closest(".faq-item").classList.toggle("open", open);
  });
});

document.querySelector("#contact-page-form")?.addEventListener("submit", (event) => {
  event.preventDefault();
  showToast("Mensagem enviada! Nossa equipe responderá em até um dia útil.");
  event.currentTarget.reset();
});

const catalogSearchForm = document.querySelector("#catalog-search-form");
const catalogSearchInput = document.querySelector("#catalog-search-input");
catalogSearchForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  state.query = catalogSearchInput.value.trim();
  elements.searchInput.value = state.query;
  renderCourses();
});
catalogSearchInput?.addEventListener("input", () => {
  state.query = catalogSearchInput.value.trim();
  elements.searchInput.value = state.query;
  renderCourses();
});

document.querySelector("#level-filter")?.addEventListener("change", (event) => {
  state.level = event.target.value;
  renderCourses();
});

const initialParams = new URLSearchParams(window.location.search);
if (document.body.dataset.page === "courses_page") {
  state.query = initialParams.get("q") ?? "";
  state.category = initialParams.get("category") ?? "all";
  state.level = initialParams.get("level") ?? "all";
  elements.searchInput.value = state.query;
  if (catalogSearchInput) catalogSearchInput.value = state.query;
  const levelFilter = document.querySelector("#level-filter");
  if (levelFilter) levelFilter.value = state.level;
}

renderCategories();
renderCourses();
renderCart();
loadApiCourses();
