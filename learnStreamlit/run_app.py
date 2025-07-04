
import streamlit.web.cli as stcli
import os
import sys

def main():
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    sys.argv = ["streamlit", "run", app_path, "--server.runOnSave=false"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()