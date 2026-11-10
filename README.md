# Poritep Partner

Многостраничный статический сайт на Eleventy + Nunjucks. Исходники хранятся в `src`, готовый сайт для GitHub Pages собирается в `dist`.

## Команды

```bash
npm install
npm run build
npm run dev
```

- `npm run build` — собрать статический сайт в `dist`.
- `npm run dev` — собрать сайт и запустить его на `http://127.0.0.1:4173`.

## Структура

```text
src/
├── _data/                   # товары и тексты переиспользуемых блоков
├── _includes/
│   ├── layouts/base.njk       # общий HTML-каркас
│   └── components/            # шапка, футер, CTA, hero, карточка товара
├── assets/                  # изображения и SVG
├── *.njk                    # страницы
├── styles.css
├── app.js
└── calculator.js
```

## Где что менять

- Шапка: `src/_includes/components/header.njk`
- Футер: `src/_includes/components/footer.njk`
- Зелёный CTA-блок: `src/_includes/components/calc-banner.njk`
- Заголовок внутренней страницы: `src/_includes/components/page-hero.njk`
- Карточка товара: `src/_includes/components/product-card.njk`
- Товары: `src/_data/products.json`
- Тексты CTA: `src/_data/ctas.json`
- Тексты заголовков страниц: `src/_data/pageHeroes.json`

Файлы в `dist` не нужно редактировать вручную: они пересобираются из `src`.
