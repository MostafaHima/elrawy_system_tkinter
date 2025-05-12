import os

project_root = os.getcwd()
excluded_dirs = {".venv", ".git", "__pycache__", ".idea", ".pytest_cache"}

for root, dirs, files in os.walk(project_root):
    # استبعاد مجلدات معينة
    dirs[:] = [d for d in dirs if d not in excluded_dirs]

    relative_dir = os.path.relpath(root, project_root)
    if relative_dir == ".":
        relative_dir = "root"

    print(f"\n📁 {relative_dir}/")

    for file in files:
        if not file.startswith(".") and not file.endswith(".pyc"):
            print(f"  └── {file}")
