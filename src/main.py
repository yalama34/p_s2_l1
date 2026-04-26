from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Iterator

from src.common.logger_config import setup_async_logger, log_writer
from src.engine.executor import AsyncTaskExecutor
from src.engine.queue import TaskQueue
from src.engine.task import Task
from src.engine.task_loader import TaskLoader
from src.sources.task_sources import APISource, FileSource, GeneratorSource
from src.handlers.priority_handler import PriorityHandler
from src.handlers.random_handler import RandomHandler


def _example_file_path() -> Path:
    return Path(__file__).resolve().parents[1] / "example.txt"


async def main() -> None:
    log_queue = setup_async_logger(logging.INFO)
    logger = logging.getLogger("main")
    writer_task = asyncio.create_task(log_writer("app.log", log_queue))

    try:
        logger.info("Initialization started...")
        loader = TaskLoader()
        loader.add_source(FileSource(str(_example_file_path())))
        loader.add_source(APISource("https://api.example.com"))
        loader.add_source(GeneratorSource(seed=42, count=10))

        def task_factory() -> Iterator[Task]:
            yield from loader.get_tasks()

        queue = TaskQueue(task_source_factory=task_factory)

        handler = RandomHandler(seed=42)

        tasks_to_process = list(queue)

        logger.info("Running asynchronous executor...")
        async with AsyncTaskExecutor(workers=3) as executor:
            executor.register_handler(handler)

            tasks_count = 0
            for task in tasks_to_process:
                await executor.submit(task)
                tasks_count += 1

            logger.info(f"Added {tasks_count} tasks from TaskQueue. Waiting for preprocessing...")
            await executor.wait_all()

        logger.info("Executor finished.")

        for task in tasks_to_process:
            logger.info(task)

        if executor.errors:
            logger.error(f"In process {len(executor.errors)} errors was encountered.")
            for i, error in enumerate(executor.errors, 1):
                logger.error(f"Error #{i}: {error}")
        else:
            logger.info("All tasks finished successfully.")
    finally:
        await log_queue.put(None)
        await writer_task



if __name__ == "__main__":
    asyncio.run(main())