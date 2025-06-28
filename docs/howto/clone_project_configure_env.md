# Clone Project and Configure Environment

## Clone project

Make sure that git is installed and you are in the folder in which you want to clone the project

```sh
git clone https://github.com/bhalshaker/fastapi-peer2peer-payments.git
```

open project folder
```sh
cd fastapi-peer2peer-payments
```

* Make sure python 3.12 is installed
```sh
python --version
```
* create venv for the project
```sh
python -m venv .venv
```

* activate venv in Windows
```sh
.venv/Script/activate
```
* activate venc in Linux/MacOS
```sh
source .venv/bin/activate
```
* install required libraries for production
```sh
pip install -r app/requirements.txt
```

* install required libraries for testing

```sh
pip install -r app/test-requirements.txt
```