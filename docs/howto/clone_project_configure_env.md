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

## Install and initilize UV in Windows

* Make sure python 3.11 is installed
```sh
python --version
```
* Install uv
```sh
pip install uv
```

Inside the project initialize uv for production/development
* Linux/Unix/macOS
```sh
unset UV_VENV
UV_VENV=.venv
uv pip 
```
* Inside the the project intialize uv for testing environment

## Install and initilize UV in Linux/macOS/Unix



## Use .devcontainers (Recommended)

### Prerequesits
