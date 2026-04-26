# Асинхронный обработчик задач

## Структура
```text
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── logger_config.py
│   ├── contracts/
│   │   ├── __init__.py
│   │   ├── contract.py
│   │   └── handler.py
│   ├── descriptors/
│   │   ├── __init__.py
│   │   └── descriptors.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── async_queue.py
│   │   ├── enums.py
│   │   ├── executor.py
│   │   ├── executor_errors.py
│   │   ├── iterator.py
│   │   ├── queue.py
│   │   ├── task.py
│   │   ├── task_errors.py
│   │   └── task_loader.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── priority_handler.py
│   │   └── random_handler.py
│   └── sources/
│       ├── __init__.py
│       └── task_sources.py
├── tests/
│   ├── conftest.py
│   ├── test_api_source.py
│   ├── test_async_queue.py
│   ├── test_descriptors.py
│   ├── test_enums.py
│   ├── test_executor.py
│   ├── test_executor_errors.py
│   ├── test_file_source.py
│   ├── test_generator_source.py
│   ├── test_handlers.py
│   ├── test_loader.py
│   ├── test_task_errors.py
│   └── test_task_queue.py
├── app.log
├── example.txt
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .coverage
└── README.md
```

## Асинхронность и логирование

В рамках данной работы была реализована асинхронная платформа обработки задач с использованием `asyncio`, добавлены механизмы централизованного неблокирующего логирования, разработана очередь для асинхронного распределения задач между воркерами и реализован паттерн обработчиков

- Асинхронный исполнитель (`AsyncTaskExecutor`): пул независимых worker-задач, которые параллельно извлекают задания из потокобезопасной очереди и передают их обработчикам
- Асинхронная очередь (`TaskAsyncQueue`): потокобезопасная очередь для передачи задач от продюсера (источника) к консьюмерам (воркерам) с поддержкой graceful shutdown (сигналы завершения)
- Обработчики (`TaskHandler`): расширяемая архитектура обработчиков на базе контрактов (`typing.Protocol`). Реализованы `PriorityHandler` (асинхронное ожидание на основе приоритета) и `RandomHandler` (симуляция ошибок)
- Неблокирующее логирование: использование стандартной библиотеки `logging` в связке с `asyncio.Queue` и `aiofiles` для асинхронной записи логов в файл без блокировки Event Loop, параллельно с выводом в консоль (`StreamHandler`)

## Запуск

```bash
uv run python src/main.py
```
## Структура Task
- `id` - идентификатор задачи
- `description` - описание
- `priority` - приоритет (от 1 до 5)
- `status` - статус задачи (new, in_progress, done, cancelled)
- `created_at` - дата создания (`default = datetime.now()`)
- `is_ready` - готова ли задача к выполнению (``priority == 5 and status == "new"``)

## Использование `@property`
В `src/engine/task.py` для полей **`id`** и **`description`** используется встроенный декоратор **`@property`**: геттер читает `_id` / `_description`, сеттер проверяет тип и инварианты (неотрицательный целый `id`, строковый `description`), делитер снимает атрибут со слота. Так публичный доступ отделён от внутреннего хранения без отдельного класса-дескриптора.

## Дескрипторы
Реализованы **три data descriptor** (есть `__get__` / `__set__`, при необходимости `__delete__`) и **один non-data descriptor** (только `__get__`) в `src/descriptors/descriptors.py`.

- **`PriorityDescriptor`** - при записи проверяет, что значение целое число в диапазоне **0–5**; иначе `InvalidPriorityError`. Читает и пишет в приватный атрибут `_*`; поддерживает удаление через `__delete__`
- **`CreatedAtDescriptor`** - при записи требует `datetime`, запрещает дату в будущем относительно `datetime.now()`, иначе `InvalidCreationDateError`. При чтении отдаёт строку с датой/временем в формате `дд.мм.гггг чч:мм:сс` (внутри по-прежнему хранится `datetime`). Удаление атрибута - через `__delete__`
- **`StatusDescriptor`** - при записи принимает только строки из набора `new`, `in_progress`, `done`, `cancelled`, иначе `InvalidStatusError`. Хранение в `_*`, удаление через `__delete__`
- **`IsReadyDescriptor`** (non-data) - только `__get__`: возвращает `True`, если у задачи `priority == 5` и `status == "new"`, иначе `False`; отдельного хранилища нет, значение вычисляется при каждом обращении

## Пользовательские исключения
В `src/engine/task_errors.py` и `src/engine/executor_errors.py` заведена иерархия **своих** исключений (наследников `Exception`), чтобы при нарушении инвариантов не использовать «голые» `ValueError`/`TypeError` без семантики.

| Класс | Когда возникает |
|-------|-----------------|
| **`TaskError`** | Базовый класс для ошибок подсистемы задач |
| **`InvalidPriorityError`** | Недопустимый приоритет (дескриптор `priority`) |
| **`InvalidCreationDateError`** | Неверный тип времени создания или дата в будущем (`created_at`) |
| **`InvalidStatusError`** | Статус не из разрешённого набора (`status`) |
| **`TaskNotFoundError`** | Задача с указанным `id` не найдена (для будущей работы с коллекциями) |
| **`TaskAlreadyExistsError`** | Попытка добавить задачу с уже существующим `id` |
| **`ExecutorError`** | Базовый класс для ошибок исполнителя задач |
| **`ExecutorNotStartedError`** | Попытка добавить задачу в незапущенный исполнитель |
| **`HandlerRegistrationError`** | Попытка обработки задачи без зарегистрированного обработчика |

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

Класс **`TaskQueue`** задаёт ленивый обход потока задач без хранения всего списка в памяти. В конструктор передаётся **фабрика** `task_source_factory: Callable[[], Iterator[Task]]` — функция без аргументов, которая при каждом вызове возвращает новый итератор по задачам (например, заново читает источники). При обходе `for task in queue:` внутри создаётся **`TaskIterator`**, который делегирует `__next__` этому итератору.

Повторный полный обход очереди снова вызывает фабрику, поэтому можно многократно итерироваться по потоку задач. Метод **`filter(mask)`** принимает предикат `mask(task) -> bool` и лениво отдаёт только подходящие задачи; если `mask` не вызываемый объект, возникает **`TypeError`**

## Тесты с покрытием
```bash
uv run pytest --cov=src --cov-report=term-missing tests/
```