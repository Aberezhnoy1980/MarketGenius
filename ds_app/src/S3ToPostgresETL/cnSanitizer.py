def sanitize_column_name(name: str) -> str:
    """
    Очищает название колонки от недопустимых символов для PostgreSQL.

    Args:
        ticker (str): Наименование тикера, которое может присутствовать в названии поля таблицы
        name (str): Исходное название колонки

    Returns:
        str: Очищенное название колонки, пригодное для использования в PostgreSQL
    """
    # # Удаляем префикс тикера (если есть)
    # if name.lower().startswith(f"{ticker.lower()}_"):
    #     name = name[len(ticker) + 1:]

    # Заменяем недопустимые символы на подчеркивание
    invalid_chars = ['%', ' ', '-', '(', ')', '/', '\\', '?', '!']
    for char in invalid_chars:
        name = name.replace(char, '_')

    # Удаляем повторяющиеся подчеркивания
    while '__' in name:
        name = name.replace('__', '_')

    # Удаляем подчеркивания в начале и конце
    name = name.strip('_')

    # Если название начинается с цифры, добавляем префикс
    if name[0].isdigit():
        name = f'col_{name}'

    return name.lower()
