from .task_sources import FileSource, APISource, GeneratorSource
from .task_loader import TaskLoader

def main():
    api_source: APISource = APISource(url="http://example.com")
    file_source: FileSource = FileSource(path="C:/labs/python/sem2/p_s2_l1/example.txt")
    generator_source: GeneratorSource = GeneratorSource(seed=13, count=5)
    loader: TaskLoader = TaskLoader()

    loader.add_source(api_source)
    loader.add_source(file_source)
    loader.add_source(generator_source)

    tasks = loader.get_tasks()
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()