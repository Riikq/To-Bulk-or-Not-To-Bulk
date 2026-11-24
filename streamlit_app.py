# Streamlit entry point wrapper for convenient execution
import runpy
from pathlib import Path

app_path = Path(__file__).parent / "src" / "to_bulk_or_not_to_bulk" / "app.py"
runpy.run_path(str(app_path), run_name="__main__")
