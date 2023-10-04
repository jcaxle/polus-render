Build Instructions
- py -m build
- py -m twine upload  dist/* or py -m twine upload --repository testpypi dist/*
- Enter __token__ as user and reference API keys for password

NOTE:
- For each upload, version name must be changed.