import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "main.py", "--server.headless=true"]
    sys.exit(stcli.main())