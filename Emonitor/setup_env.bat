winget install --id=OpenJS.NodeJS.LTS -e --source winget
winget install --id=Python.Python.3 -e --source winget
refreshenv
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
npm install
