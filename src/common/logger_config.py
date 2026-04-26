import asyncio
import logging
import sys

import aiofiles


async def log_writer(path: str, queue: "asyncio.Queue[str | None]") -> None:
    async with aiofiles.open(path, mode="a", encoding="utf-8") as file:
        while True:
            line = await queue.get()
            if line is None:
                queue.task_done()
                break
            await file.write(line)
            if not line.endswith("\n"):
                await file.write("\n")
            await file.flush()

            if not line.endswith("\n"):
                line += "\n"
            await asyncio.to_thread(sys.stdout.write, line)
            await asyncio.to_thread(sys.stdout.flush)

            queue.task_done()


class AsyncQueueHandler(logging.Handler):
    def __init__(self, queue: "asyncio.Queue[str | None]"):
        super().__init__()
        self.queue = queue

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.queue.put_nowait(msg)
        except Exception:
            self.handleError(record)


def setup_async_logger(level: int = logging.INFO) -> "asyncio.Queue[str | None]":
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    queue_handler = AsyncQueueHandler(queue)
    queue_handler.setFormatter(
        logging.Formatter(
            "[%(name)s] (%(asctime)s): %(message)s",
            datefmt="%d.%m.%Y %H:%M:%S",
        )
    )
    root_logger.addHandler(queue_handler)

    return queue
