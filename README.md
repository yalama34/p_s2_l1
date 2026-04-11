# Лабораторная работа №2. Модель задачи: дескрипторы и @property

## Цель
Освоить управление доступом к атрибутам и защиту инвариантов доменной модели на примере класса `Task` в платформе обработки задач: пользовательские дескрипторы, `property`, разделение публичного API и внутреннего состояния, специализированные исключения.

## Структура
```
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── contracts/
│   │   ├── __init__.py
│   │   └── contract.py
│   ├── descriptors/
│   │   ├── __init__.py
│   │   └── descriptors.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── iterator.py
│   │   ├── queue.py
│   │   ├── task.py
│   │   ├── task_errors.py
│   │   └── task_loader.py
│   └── sources/
│       ├── __init__.py
│       └── task_sources.py
├── tests/
│   ├── conftest.py
│   ├── test_api_source.py
│   ├── test_descriptors.py
│   ├── test_enums.py
│   ├── test_file_source.py
│   ├── test_generator_source.py
│   ├── test_loader.py
│   ├── test_task_errors.py
│   └── test_task_queue.py
├── example.txt
├── pyproject.toml
├── .gitignore
├── .coverage
└── README.md
```

## Запуск

```bash
python -m src.main
```
## Структура Task
- `id` - идентификатор задачи
- `description` - описание
- `priority` - приоритет (от 1 до 5)
- `status` - статус задачи (new, in_progress, done, cancelled)
- `created_at` - дата создания (`default = datetime.now()`)
- `is_ready` - готова ли задача к выполнению (``priority == 5 and status == "new"``)

## Использование `@property`
В `src/task_engine/task.py` для полей **`id`** и **`description`** используется встроенный декоратор **`@property`**: геттер читает `_id` / `_description`, сеттер проверяет тип и инварианты (неотрицательный целый `id`, строковый `description`), делитер снимает атрибут со слота. Так публичный доступ отделён от внутреннего хранения без отдельного класса-дескриптора.

## Дескрипторы
Реализованы **три data descriptor** (есть `__get__` / `__set__`, при необходимости `__delete__`) и **один non-data descriptor** (только `__get__`) в `src/descriptors/descriptors.py`.

- **`PriorityDescriptor`** - при записи проверяет, что значение целое число в диапазоне **0–5**; иначе `InvalidPriorityError`. Читает и пишет в приватный атрибут `_*`; поддерживает удаление через `__delete__`
- **`CreatedAtDescriptor`** - при записи требует `datetime`, запрещает дату в будущем относительно `datetime.now()`, иначе `InvalidCreationDateError`. При чтении отдаёт строку с датой/временем в формате `дд.мм.гггг чч:мм:сс` (внутри по-прежнему хранится `datetime`). Удаление атрибута - через `__delete__`
- **`StatusDescriptor`** - при записи принимает только строки из набора `new`, `in_progress`, `done`, `cancelled`, иначе `InvalidStatusError`. Хранение в `_*`, удаление через `__delete__`
- **`IsReadyDescriptor`** (non-data) - только `__get__`: возвращает `True`, если у задачи `priority == 5` и `status == "new"`, иначе `False`; отдельного хранилища нет, значение вычисляется при каждом обращении

## Пользовательские исключения
В `src/task_engine/task_errors.py` заведена иерархия **своих** исключений (наследников `Exception`), чтобы при нарушении инвариантов не использовать «голые» `ValueError`/`TypeError` без семантики.

| Класс | Когда возникает |
|-------|-----------------|
| **`TaskError`** | Базовый класс для ошибок подсистемы задач |
| **`InvalidPriorityError`** | Недопустимый приоритет (дескриптор `priority`) |
| **`InvalidCreationDateError`** | Неверный тип времени создания или дата в будущем (`created_at`) |
| **`InvalidStatusError`** | Статус не из разрешённого набора (`status`) |
| **`TaskNotFoundError`** | Задача с указанным `id` не найдена (для будущей работы с коллекциями) |
| **`TaskAlreadyExistsError`** | Попытка добавить задачу с уже существующим `id` |

В тестах и коде дескрипторов эти типы позволяют точно перехватывать сбой валидации (`pytest.raises(InvalidPriorityError)` и т.п.)

## Подсистема приёма задач

## Типы источников задач
1. **FileSource** — загрузка из файла по шаблону строки (пример в `example.txt`).
2. **GeneratorSource** — псевдослучайный набор задач с фиксированным seed.
3. **APISource** — заглушка внешнего API с данными в памяти.

## Контракт источника
Все источники реализуют единый протокол без общего базового класса:

```python
@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> List[Task]:
        """Return zero or more tasks from this source."""
        ...
```

## Очередь задач `TaskQueue`

Класс **`TaskQueue`** (`src/engine/queue.py`) задаёт ленивый обход потока задач без хранения всего списка в памяти. В конструктор передаётся **фабрика** `task_source_factory: Callable[[], Iterator[Task]]` — функция без аргументов, которая при каждом вызове возвращает новый итератор по задачам (например, заново читает источники). При обходе `for task in queue:` внутри создаётся **`TaskIterator`**, который делегирует `__next__` этому итератору.

Повторный полный обход очереди снова вызывает фабрику, поэтому можно многократно проходить по «свежему» потоку задач. Метод **`filter(mask)`** принимает предикат `mask(task) -> bool` и лениво отдаёт только подходящие задачи; если `mask` не вызываемый объект, возникает **`TypeError`**.

## Тесты с покрытием
```bash
pytest --cov=src --cov-report=term-missing tests/
```

## Тестирование
Пример отчёта о покрытии (значения зависят от текущей версии кода):

```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src\__init__.py                      0      0   100%
src\contracts\__init__.py            0      0   100%
src\contracts\contract.py            5      0   100%
src\descriptors\__init__.py          0      0   100%
src\descriptors\descriptors.py      53      0   100%
src\engine\__init__.py               0      0   100%
src\engine\enums.py                 17      0   100%
src\engine\iterator.py              10      0   100%
src\engine\queue.py                 14      0   100%
src\engine\task.py                  41      5    88%   42, 53, 62, 67, 71
src\engine\task_errors.py           27      0   100%
src\engine\task_loader.py           16      0   100%
src\main.py                         27     27     0%   3-42
src\sources\__init__.py              0      0   100%
src\sources\task_sources.py         59      1    98%   18
--------------------------------------------------------------
TOTAL                              269     33    88%
```

## Вывод
Реализован класс `Task` с разделением внутреннего состояния и публичного API, валидацией через пользовательские **data descriptors** и **`property`**, специализированными исключениями при нарушении инвариантов; сохранена расширяемая подсистема источников задач на основе **`typing.Protocol`** и runtime-проверки контракта.
