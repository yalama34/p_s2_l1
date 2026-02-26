from .task_sources import FileSource, APISource, GeneratorSource
from .task_loader import TaskLoader

def main():
    api_source: APISource = APISource(url="http://example.com")
    file_source: FileSource = FileSource(path="/p_s2_l1/tests/example.txt")
    generator_source: GeneratorSource = GeneratorSource(seed=13, count=5)
    loader: TaskLoader = TaskLoader()

    loader.add_source(api_source)
    loader.add_source(file_source)
    loader.add_source(generator_source)

    print(loader.get_tasks())


if __name__ == "__main__":
    main()