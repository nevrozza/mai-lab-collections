# Python. Лабораторная работа 4
### Симуляция и пользовательские коллекции (Библиотека)
- **Библиотеки:**
  - `random` – _Псевдослучайность_
  - `collections` - _defaultdict_
  - `dataclasses`, `enum`, `abc`, `pytest`
    
- **Интересные штучки:**
  - Тесты не только для `Library`, `IndexDict`, `BookCollection`, но и для симуляции
  - Запрещены дубликаты
  - `LibraryPanel` – одна из реализаций `LibraryABC`, представляет собой некое CLI для `Library`
  - Для красоты кода был создан класс `SimulationEventHandlers`, который помогает заменить `if-else` конструкцию на `dict`
  - Методы возвращают `ImmutableBookCollection` – невозможно отредактировать оригинал

### Что нового я познал?
- До конца разобрался с тем, как работают `gc` и объекты в `Python`
- Изучил стандартные коллекции
- Научился писать `overload` функции и методы

## Структура проекта
```
todo
```


## Quick start
 0) Установить `uv` _0_o_
 1) Клонировать этот репозиторий через git и активировать uv:
   ```
   git clone https://github.com/nevrozza/mai-lab-collections
   cd mai-lab-collections
   uv sync
   ```
 2) Запустить программу через `uv`:
    `uv run -m src.main`
 3) Вы великолепны!
