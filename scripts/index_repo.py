from pathlib import Path

if __name__ == '__main__':
    project_root = Path(__file__).resolve().parent.parent
    files = [str(path.relative_to(project_root)) for path in project_root.rglob('*.py')]
    print(f'Indexed {len(files)} Python files')
    for path in files:
        print(path)
