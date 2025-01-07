import os
import importlib.util

class ModuleEditor:
    def __init__(self, module_name):
        self.module_name = module_name
        
        self.base_dir = self._find_module_base_dir()
        self.frontend_dir = os.path.join(self.base_dir, 'frontend')

        # Use a temporary directory for the index.html file if writing fails
        self.index_html_path = "/tmp/index.html"  # Temporary writable directory

    def _find_module_base_dir(self):
        """Find the base directory of the module."""
        spec = importlib.util.find_spec(self.module_name)
        if spec is None:
            raise ImportError(f"Module {self.module_name} not found")
        return os.path.dirname(spec.origin)

    def read_file(self, file_path):
        """Read the contents of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def write_file(self, file_path, content):
        """Write content to a file, creating directories if necessary."""
        try:
            # Ensure the directory exists
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)  # Create the directory if it doesn't exist

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"File written successfully to {file_path}")
        except PermissionError as e:
            print(f"PermissionError: Unable to write to {file_path}. Please check permissions. {e}")
        except IOError as e:
            print(f"IOError: Unable to write to {file_path}. {e}")

    def modify_index_html(self):
        """Modify the index.html file."""
        new_index_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>st-copy-to-clipboard</title>
  <script src="./streamlit-component-lib.js"></script>
  <script src="./main.js"></script>
  <style>
    /* Dark mode styles */
    body.dark-mode {
      background-color: #0e1117;
      color: #fff;
    }
  </style>
</head>
<body class="dark-mode">
  <div id="root">
    <button id="text-element" class="st-copy-to-clipboard-btn"></button>
    <button id="copy-button" class="st-copy-to-clipboard-btn">📋</button>
  </div>
</body>
</html>
            """
        self.write_file(self.index_html_path, new_index_html_content.strip())

    def modify_frontend_files(self):
        """Modify all necessary frontend files, including index.html."""
        self.modify_index_html()
