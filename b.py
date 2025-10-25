import ast
import pkg_resources

# Path to your app.py file (Change this if needed)
file_path = "app.py"

def get_imported_libraries(file_path):
    """Extracts all imported libraries from a Python file."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    imported_libs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_libs.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imported_libs.add(node.module)

    return imported_libs

def get_installed_versions(imported_libs):
    """Matches imported libraries with installed versions."""
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    imported_versions = {lib: installed_packages.get(lib.lower(), "Not Installed") for lib in imported_libs}
    
    return imported_versions

# Get imported libraries from app.py
imported_libs = get_imported_libraries(file_path)

# Get installed versions
imported_lib_versions = get_installed_versions(imported_libs)

print("\nLibraries used in app.py with versions:")
for lib, version in imported_lib_versions.items():
    print(f"{lib}: {version}")
