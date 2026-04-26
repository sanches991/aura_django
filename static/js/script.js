/* =============================================================
   AURA — Fine Dining | Menu logic
   ВСЕ ДАННЫЕ О БЛЮДАХ ТЕПЕРЬ НАХОДЯТСЯ В HTML (index.html).
   JavaScript отвечает только за поведение:
     - переключение категорий / фильтр
     - поиск по карточкам
     - корзина (добавить / убавить / удалить)
     - модальное окно блюда (состав/описание)
     - мобильный поиск, выдвижная строка
   ============================================================= */

/* ---------------------- STATE ---------------------- */
const state = {
  activeCat: 'all',
  search: '',          /* текущий поисковый запрос */
  /** cart: { [dishId]: qty } */
  cart: {}
};

/* ---------------------- DOM REFS ---------------------- */
const $grid        = document.getElementById('dishGrid');
const $gridEmpty   = document.getElementById('gridEmpty');
const $navItems    = document.querySelectorAll('.nav-item');
const $catChips    = document.querySelectorAll('.cat-chip');
const $dishSections = document.querySelectorAll('.dish-section');

const $cartPill    = document.getElementById('cartPill');
const $mobileCart  = document.getElementById('mobileCartBtn');
const $cartPanel   = document.getElementById('cartPanel');
const $cartOverlay = document.getElementById('cartOverlay');
const $cartClose   = document.getElementById('cartClose');
const $continueBtn = document.getElementById('continueBtn');

const $cartBody    = document.getElementById('cartBody');
const $cartEmpty   = document.getElementById('cartEmpty');
const $cartFoot    = document.getElementById('cartFoot');
const $cartTotal   = document.getElementById('cartTotal');

const $pillBadge   = document.getElementById('cartPillBadge');
const $mobBadge    = document.getElementById('mobileCartBadge');

const $toast       = document.getElementById('toast');

/* ---------------------- CATEGORY NAME MAP (для бейджа в модалке) ---------------------- */
/* Переводы ярлыков категорий нужны только для модального окна */
const catNames = {
  salads: 'Салаты',
  mains: 'Основные блюда',
  desserts: 'Десерты',
  drinks: 'Напитки'
};

/* ---------------------- HELPERS: читаем данные блюда ИЗ DOM ---------------------- */
/* Все данные о блюдах хранятся в самих HTML-карточках:
     • data-id            — идентификатор
     • data-category      — категория
     • data-price         — цена (число)
     • .card-name         — название
     • .card-desc         — описание
     • .card-media img    — изображение
     • .card-ingredients-data li — состав (список)
*/

function getCardById(id) {
  return document.querySelector(`.card[data-id="${id}"]`);
}

/* Возвращает объект с данными блюда, прочитанными из DOM-карточки */
function getDish(id) {
  const card = getCardById(id);
  if (!card) return null;
  return {
    id:    card.dataset.id,
    cat:   card.dataset.category,
    price: parseInt(card.dataset.price, 10) || 0,
    name:  card.querySelector('.card-name').textContent.trim(),
    desc:  card.querySelector('.card-desc').textContent.trim(),
    img:   card.querySelector('.card-media img').getAttribute('src')
  };
}

/* ---------------------- РЕНДЕР СЕТКИ (фильтрация показ/скрытие) ---------------------- */
/* Карточки никогда не создаются из JS — они уже есть в HTML.
   Здесь мы только скрываем/показываем их в зависимости от категории и поиска. */
function renderGrid(){
  const isAll = state.activeCat === 'all';
  const term  = state.search.toLowerCase().trim();

  $grid.style.opacity = 0;
  setTimeout(() => {
    let visibleCount = 0;

    /* ---- Фильтрация карточек ---- */
    document.querySelectorAll('.card[data-id]').forEach(card => {
      const cat  = card.dataset.category;
      const name = card.querySelector('.card-name').textContent.toLowerCase();
      const desc = card.querySelector('.card-desc').textContent.toLowerCase();
      const matchCat    = isAll || cat === state.activeCat;
      const matchSearch = !term || name.includes(term) || desc.includes(term);
      const visible     = matchCat && matchSearch;
      card.style.display = visible ? '' : 'none';
      if (visible) visibleCount++;
    });

    /* ---- Секции: заголовки только при режиме "Все блюда" без поиска ---- */
    $dishSections.forEach(section => {
      const secVisible = Array.from(section.querySelectorAll('.card'))
                              .some(c => c.style.display !== 'none');

      /* Скрываем/показываем саму секцию */
      section.style.display = secVisible ? '' : 'none';

      /* Заголовок секции показываем только в режиме "все блюда" без поискового запроса */
      const head = section.querySelector('.dish-section-head');
      if (head) {
        const showHead = isAll && !term;
        head.style.display = showHead ? '' : 'none';
      }
    });

    /* ---- Пустое состояние поиска ---- */
    if ($gridEmpty) {
      $gridEmpty.hidden = !(term && visibleCount === 0);
    }

    /* ---- Перезапуск анимации у видимых карточек (для эффекта фильтра) ---- */
    const visibleCards = Array.from(document.querySelectorAll('.card[data-id]'))
                              .filter(c => c.style.display !== 'none');
    visibleCards.forEach((card, i) => {
      card.style.animation = 'none';
      /* reflow, чтобы анимация запустилась заново */
      void card.offsetWidth;
      card.style.animation = '';
      card.style.animationDelay = (i * 55) + 'ms';
    });

    $grid.style.opacity = 1;
    updateCardQtyDisplays(); /* восстановить счётчики после перерисовки */
  }, 140);
}

/* ---------------------- CATEGORY SWITCH ---------------------- */
function setCategory(cat){
  state.activeCat = cat;
  $navItems.forEach(b => b.classList.toggle('is-active', b.dataset.category === cat));
  $catChips.forEach(b => b.classList.toggle('is-active', b.dataset.category === cat));
  renderGrid();
}
$navItems.forEach(b => {
  /* "Ознакомление" — это <a>, у него нет data-category, пропускаем */
  if (!b.dataset.category) return;
  b.addEventListener('click', () => setCategory(b.dataset.category));
});
const $catScroll = document.querySelector('.cat-scroll');

$catChips.forEach(b => {
  if (!b.dataset.category) return;
  b.addEventListener('click', () => {
    setCategory(b.dataset.category);
    /* Скроллим только горизонтально внутри контейнера —
       scrollIntoView трогает вертикаль страницы, что ломает позиционирование */
    if ($catScroll) {
      const scrollLeft = b.offsetLeft - ($catScroll.offsetWidth - b.offsetWidth) / 2;
      $catScroll.scrollTo({left: scrollLeft, behavior: 'smooth'});
    }
  });
});

/* ---------------------- CART OPERATIONS ---------------------- */
function addToCart(id){
  state.cart[id] = (state.cart[id] || 0) + 1;
  renderCart();
  showToast('Добавлено в корзину');
}

function changeQty(id, delta){
  if(!state.cart[id]) return;
  state.cart[id] += delta;
  if(state.cart[id] <= 0) delete state.cart[id];
  renderCart();
}

function removeFromCart(id){
  delete state.cart[id];
  renderCart();
}

/* ---------------------- RENDER CART ---------------------- */
/* В корзине строки формируются динамически по мере добавления блюд пользователем.
   ВАЖНО: данные блюда берутся ИЗ DOM-карточек, а не из JS-массива. */
function renderCart(){
  const ids   = Object.keys(state.cart);
  const count = ids.reduce((s, id) => s + state.cart[id], 0);
  const total = ids.reduce((s, id) => {
    const d = getDish(id);
    return d ? s + d.price * state.cart[id] : s;
  }, 0);

  // Бейджи
  $pillBadge.textContent = count;
  $mobBadge.textContent  = count;
  $pillBadge.style.display = count ? '' : 'none';
  $mobBadge.style.display  = count ? '' : 'none';

  // Пусто vs содержимое
  if(!ids.length){
    $cartEmpty.style.display = 'flex';
    $cartBody.querySelectorAll('.cart-item').forEach(el => el.remove());
    $cartFoot.hidden = true;
    updateCardQtyDisplays(); /* сбросить все счётчики на карточках */
    return;
  }
  $cartEmpty.style.display = 'none';
  $cartFoot.hidden = false;
  $cartTotal.textContent = total.toLocaleString('ru-RU');

  // Очистить и перестроить строки корзины
  $cartBody.querySelectorAll('.cart-item').forEach(el => el.remove());
  ids.forEach(id => {
    const d = getDish(id);
    if(!d) return;
    const qty = state.cart[id];
    const itemHtml = `
      <div class="cart-item" data-id="${d.id}">
        <div class="cart-thumb"><img src="${d.img}" alt="" loading="lazy"></div>
        <div class="cart-info">
          <h4 class="cart-name">${escapeHtml(d.name)}</h4>
          <div class="qty">
            <button data-action="dec" aria-label="Уменьшить">−</button>
            <span>${qty}</span>
            <button data-action="inc" aria-label="Увеличить">+</button>
          </div>
        </div>
        <div class="cart-right">
          <button class="cart-remove" data-action="remove" aria-label="Удалить">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6"/><path d="M6 7l1 12a2 2 0 0 0 2 1.8h6a2 2 0 0 0 2-1.8l1-12"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/></svg>
          </button>
          <div class="cart-price">${(d.price * qty).toLocaleString('ru-RU')} сом</div>
        </div>
      </div>
    `;
    $cartBody.insertAdjacentHTML('beforeend', itemHtml);
  });

  // Привязка + / − / удалить
  $cartBody.querySelectorAll('.cart-item').forEach(row => {
    const id = row.dataset.id;
    row.querySelector('[data-action="dec"]').addEventListener('click', () => changeQty(id, -1));
    row.querySelector('[data-action="inc"]').addEventListener('click', () => changeQty(id, +1));
    row.querySelector('[data-action="remove"]').addEventListener('click', () => removeFromCart(id));
  });

  updateCardQtyDisplays(); /* синхронизировать счётчики на карточках с корзиной */
}

/* ---------------------- CART PANEL TOGGLE ---------------------- */
function openCart(){
  $cartPanel.classList.add('is-open');
  $cartOverlay.classList.add('is-open');
  $cartPanel.setAttribute('aria-hidden', 'false');
  $cartOverlay.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}
function closeCart(){
  $cartPanel.classList.remove('is-open');
  $cartOverlay.classList.remove('is-open');
  $cartPanel.setAttribute('aria-hidden', 'true');
  $cartOverlay.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}
$cartPill.addEventListener('click', openCart);
$mobileCart.addEventListener('click', openCart);
$cartClose.addEventListener('click', closeCart);
$cartOverlay.addEventListener('click', closeCart);
$continueBtn.addEventListener('click', closeCart);
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape' && $cartPanel.classList.contains('is-open')) closeCart();
});

/* ---------------------- TOAST ---------------------- */
let toastTimer = null;
function showToast(text){
  $toast.textContent = text;
  $toast.classList.add('is-visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $toast.classList.remove('is-visible'), 1600);
}

/* ---------------------- HELPERS ---------------------- */
function escapeHtml(str){
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/* ---------------------- INIT ---------------------- */
/* Сетка уже отрисована в HTML — достаточно проинициализировать корзину.
   renderGrid вызывается только при изменении фильтра/поиска. */
renderCart();

/* =============================================================
   DISH MODAL — модальное окно с подробной информацией о блюде
   Данные (название, описание, цена, картинка, состав) читаются
   напрямую из HTML-карточки.
   ============================================================= */

/* ---- DOM refs ---- */
const $dishOverlay = document.getElementById('dishOverlay');
const $dishModal   = document.getElementById('dishModal');
const $dishClose   = document.getElementById('dishModalClose');
const $dishAdd     = document.getElementById('dishModalAdd');

let _modalDishId = null;

/* ---- Open modal ---- */
function openDishModal(id) {
  const card = getCardById(id);
  if (!card) return;
  const d = getDish(id);
  if (!d) return;
  _modalDishId = id;

  /* Заполнить контент из данных карточки */
  const photo = document.getElementById('dishModalPhoto');
  photo.src = d.img;
  photo.alt = d.name;
  document.getElementById('dishModalCat').textContent   = catNames[d.cat] || '';
  document.getElementById('dishModalTitle').textContent = d.name;
  document.getElementById('dishModalPrice').innerHTML   =
    `${d.price.toLocaleString('ru-RU')} <em>сом</em>`;
  document.getElementById('dishModalDesc').textContent  = d.desc;

  /* Состав — копируем <li>-элементы из скрытого списка карточки в модалку */
  const modalIngs = document.getElementById('dishModalIngredients');
  modalIngs.textContent = ''; /* очистить */
  const sourceList = card.querySelector('.card-ingredients-data');
  if (sourceList) {
    sourceList.querySelectorAll('li').forEach(li => {
      modalIngs.appendChild(li.cloneNode(true));
    });
  }

  /* Показать */
  $dishOverlay.classList.add('is-open');
  $dishModal.classList.add('is-open');
  $dishOverlay.setAttribute('aria-hidden', 'false');
  $dishModal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

/* ---- Close modal ---- */
function closeDishModal() {
  $dishOverlay.classList.remove('is-open');
  $dishModal.classList.remove('is-open');
  $dishOverlay.setAttribute('aria-hidden', 'true');
  $dishModal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  _modalDishId = null;
}

/* ---- Event listeners ---- */
$dishClose.addEventListener('click', closeDishModal);
$dishOverlay.addEventListener('click', closeDishModal);

$dishAdd.addEventListener('click', () => {
  if (_modalDishId) {
    addToCart(_modalDishId);   /* вызов существующей функции */
    closeDishModal();
  }
});

/* Escape key (не конфликтует — у корзины своя проверка) */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && $dishModal.classList.contains('is-open')) closeDishModal();
});

/* Клик по карточке — делегирование всех действий */
$grid.addEventListener('click', (e) => {
  /* Кнопка "−" — убавить количество в корзине */
  const decBtn = e.target.closest('.card-qty-dec');
  if (decBtn) { changeQty(decBtn.dataset.id, -1); return; }

  /* Кнопка "+" контрола — добавить ещё одну единицу */
  const incBtn = e.target.closest('.card-qty-inc');
  if (incBtn) { addToCart(incBtn.dataset.id); return; }

  /* Кнопка "Подробнее" — открыть модал с составом */
  const moreBtn = e.target.closest('.card-more');
  if (moreBtn) { openDishModal(moreBtn.dataset.id); return; }

  /* Кнопка "+" (первое добавление в корзину) */
  const addBtn = e.target.closest('.card-add');
  if (addBtn) {
    const id = addBtn.dataset.id;
    addToCart(id);
    /* tiny pop */
    addBtn.animate(
      [{transform:'scale(1)'},{transform:'scale(1.25)'},{transform:'scale(1)'}],
      {duration:280, easing:'cubic-bezier(.34,1.56,.64,1)'}
    );
    return;
  }

  /* Клик по карточке (не по кнопкам) → открыть модальное окно */
  const card = e.target.closest('.card');
  if (!card) return;
  const btn = card.querySelector('.card-add[data-id]');
  if (btn) openDishModal(btn.dataset.id);
});

/* =============================================================
   ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
   ============================================================= */

/* --- Синхронизировать счётчики количества на карточках с корзиной --- */
/* Итерируемся по существующим DOM-карточкам (а не по JS-массиву) */
function updateCardQtyDisplays() {
  document.querySelectorAll('.card[data-id]').forEach(card => {
    const id     = card.dataset.id;
    const ctrl   = card.querySelector(`#qty-ctrl-${id}`);
    const numEl  = card.querySelector(`#qty-num-${id}`);
    const addBtn = card.querySelector(`.card-add[data-id="${id}"]`);
    if (!ctrl) return;
    const qty = state.cart[id] || 0;
    if (qty > 0) {
      ctrl.style.display   = 'flex';
      if (addBtn) addBtn.style.display = 'none';
      if (numEl)  numEl.textContent    = qty;
    } else {
      ctrl.style.display   = 'none';
      if (addBtn) addBtn.style.display = '';
    }
  });
}

/* --- Счётчики блюд рядом с категориями в сайдбаре --- */
/* Значения уже прописаны в HTML (<span class="nav-count">4</span>),
   поэтому здесь ничего делать не нужно. Функция больше не вызывается. */

/* --- Поиск в реальном времени --- */
const $searchInput = document.getElementById('searchInput');
const $searchClear = document.getElementById('searchClear');

if ($searchInput) {
  $searchInput.addEventListener('input', () => {
    state.search = $searchInput.value;
    /* Показать/скрыть кнопку очистки */
    if ($searchClear) $searchClear.hidden = !state.search;
    renderGrid();
  });
}

if ($searchClear) {
  $searchClear.addEventListener('click', () => {
    $searchInput.value = '';
    state.search = '';
    $searchClear.hidden = true;
    $searchInput.focus();
    renderGrid();
  });
}

/* =============================================================
   МОБИЛЬНЫЙ ПОИСК — раскрывающаяся строка под хедером
   ============================================================= */

const $mobileSearchBtn   = document.getElementById('mobileSearchBtn');
const $mobileSearchBar   = document.getElementById('mobileSearchBar');
const $mobileSearchInput = document.getElementById('mobileSearchInput');
const $mobileSearchClear = document.getElementById('mobileSearchClear');

/* Переключатель видимости мобильной строки поиска */
if ($mobileSearchBtn) {
  $mobileSearchBtn.addEventListener('click', () => {
    const isOpen = $mobileSearchBar.classList.toggle('is-open');
    $mobileSearchBar.setAttribute('aria-hidden', String(!isOpen));
    $mobileSearchBtn.classList.toggle('is-active', isOpen);
    document.body.classList.toggle('mobile-search-open', isOpen);
    if (isOpen) {
      /* Небольшая задержка — дать анимации развернуться */
      setTimeout(() => $mobileSearchInput && $mobileSearchInput.focus(), 160);
    } else {
      /* Закрытие — сбросить запрос */
      if ($mobileSearchInput) $mobileSearchInput.value = '';
      state.search = '';
      if ($mobileSearchClear) $mobileSearchClear.hidden = true;
      renderGrid();
    }
  });
}

/* Поиск из мобильного поля — синхронизируется с тем же state.search */
if ($mobileSearchInput) {
  $mobileSearchInput.addEventListener('input', () => {
    state.search = $mobileSearchInput.value;
    if ($mobileSearchClear) $mobileSearchClear.hidden = !state.search;
    /* Синхронизировать с десктопным полем */
    const $di = document.getElementById('searchInput');
    if ($di) $di.value = state.search;
    renderGrid();
  });
}

if ($mobileSearchClear) {
  $mobileSearchClear.addEventListener('click', () => {
    if ($mobileSearchInput) $mobileSearchInput.value = '';
    state.search = '';
    $mobileSearchClear.hidden = true;
    if ($mobileSearchInput) $mobileSearchInput.focus();
    /* Синхронизировать с десктопным полем */
    const $di = document.getElementById('searchInput');
    if ($di) $di.value = '';
    renderGrid();
  });
}
