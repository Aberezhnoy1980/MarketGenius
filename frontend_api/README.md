# Клиентское приложение проекта Market Genius

Фреймворк для разработки клиентской части приложения - react. 

Приложение разрабатывается  в соответствии с методологией БЭМ (блок - элемент - модификатор). Данный подход предполагает разделение кодовой базы на логические элементы и за счет инкапсуляции позволяет эффективно переиспользовать элементы интерфейсов, а также поддерживать и масштабировать проект, обеспечивая высокую производительность разработки. 

Стилизация интерфейсов и элементов организована интеграцией каскадных таблиц стилей скомпилированных препроцессором SCSS. Такая схема обеспечивает преимущества возможностей препроцессора и эффективную синхронизацию с БЭМ-структурой приложения.

В проекте активно используются современные и передовые технологии CSS3 и HTML5, такие как псевдоклассы и псевдоэлементы, адаптивная верстка, анимация и другие.

Позиционирование элементов и блоков приложения, преимущественно организовано на технологии flexbox. Верстка является адаптивной, что позволяет комфортно пользоваться приложениях на устройствах с разным экранным разрешением, в том числе и на мобильных устройствах, что в свою очередь на ранних этапах развития проекта частично компенсирует отсутствие мобильного приложения.

Сборщиком приложения является vite.

Все интерфейсы приложения выделены в отдельные блоки (БЭМ) и являются в то же время компонентами react.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
