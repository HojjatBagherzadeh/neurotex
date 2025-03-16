import ast
import os

def extract_function_code(repo_path: str, module_function: str) -> str:
    """
    Expecting format: "module_name.function_name"
    For this function we only analyze the python files. (we can extend to other types.)
    """
    parts = module_function.split(".")
    if len(parts) != 2:
        raise ValueError("Invalid function name format. Expected 'module_name.function_name'")
    module_name, function_name = parts
    file_path = os.path.join(repo_path, f"{module_name}.py")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Module {module_name}.py not found in repository")
    with open(file_path, "r") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Attempt to extract the source code of the function.
            function_code = ast.get_source_segment(source, node)
            if function_code is None:
                # Fallback extraction using line numbers.
                lines = source.splitlines()
                function_code = "\n".join(lines[node.lineno-1: node.end_lineno])
            return function_code
    raise ValueError(f"Function {function_name} not found in module {module_name}")
