from pathlib import Path
from shutil import copyfile

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    example = root / '.env.example'
    target = root / '.env'
    if not target.exists() and example.exists():
        copyfile(example, target)
        print('Created .env from .env.example')
    else:
        print('.env already exists or .env.example is missing')
