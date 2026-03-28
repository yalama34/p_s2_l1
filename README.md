# Лабораторная работа №2. Модель задачи: дескрипторы и @property

## Цель
Освоить управление доступом к атрибутам и защиту инвариантов доменной модели на примере класса `Task` в платформе обработки задач: пользовательские дескрипторы, `property`, разделение публичного API и внутреннего состояния, специализированные исключения.

## Структура
```
├── src/
│   ├── __init__.py                 
│   ├── main.py                     
│   ├── descriptors/
│   │   ├── __init__.py
│   │   └── descriptors.py          
│   └── task_engine/
│       ├── __init__.py
│       ├── task.py                 
│       ├── task_errors.py         
│       ├── contract.py             
│       ├── task_loader.py          
│       └── task_sources.py         
├── tests/
│   ├── conftest.py                 
│   ├── test_descriptors.py         
│   ├── test_file_source.py
│   ├── test_generator_source.py
│   ├── test_api_source.py
│   └── test_loader.py
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

## Типы источников задач (лаб. №1)
1. **FileSource** — загрузка из файла по шаблону строки (пример в `example.txt`).
2. **GeneratorSource** — псевдослучайный набор задач с фиксированным seed.
3. **APISource** — заглушка внешнего API с данными в памяти.

## Контракт источника (лаб. №1)
Все источники реализуют единый протокол без общего базового класса:

```python
@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> List[Task]:
        """Return zero or more tasks from this source."""
        ...
```

## Тесты с покрытием
```bash
pytest --cov=src --cov-report=term-missing tests/
```

## Тестирование
Пример отчёта о покрытии (значения зависят от текущей версии кода):

```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src\__init__.py                       0      0   100%
src\descriptors\__init__.py           0      0   100%
src\descriptors\descriptors.py       54      7    87%   22, 33, 44, 60, 73, 83, 89
src\main.py                          18     18     0%   1-26
src\task_engine\__init__.py           0      0   100%
src\task_engine\contract.py           5      0   100%
src\task_engine\task.py              43      4    91%   43, 60, 69, 74
src\task_engine\task_errors.py       23      4    83%   16-17, 24-25
src\task_engine\task_loader.py       17      0   100%
src\task_engine\task_sources.py      59      0   100%
---------------------------------------------------------------
TOTAL                               219     33    85%
```

## Вывод
Реализован класс `Task` с разделением внутреннего состояния и публичного API, валидацией через пользовательские **data descriptors** и **`property`**, специализированными исключениями при нарушении инвариантов; сохранена расширяемая подсистема источников задач на основе **`typing.Protocol`** и runtime-проверки контракта.
