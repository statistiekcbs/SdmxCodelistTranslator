# Sdmx Codelist Translator
Get a SDMX codelist from a remote repository and translate it into your favourite language.

translate.py uses online resources

translate-hub.py uses local Hugging Face model
Please check cudacheck.py for available GPU resources

Use python 3.11 or lower. Transformers and other dependencies are not available (yet) for 3.12

# Setup VS Code
## clone repo : 
```
git clone https://github.com/statistiekcbs/SdmxCodelistTranslator.git
```
## create a virtual environment (venv)
- in Visual Code : F1 -> Python Create Environment ...
- CLI
```
python -m venv .
```

## install packages
- CLI : 
```
pip -r requirements.txt
```
- VS Code : Mark requirements.txt checkbox during creation of the virtual environment
