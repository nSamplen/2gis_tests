"# 2gis_tests" 
## Creating Virtual Environments
```
python -m venv tutorial-env
```
Run 
```
tutorial-env\Scripts\activate.bat
```
Install all the necessary packages from requirements.txt file
```
python -m pip install -r requirements.txt
```

## Run tests
```
pytest -v -s gisTests.py
```
