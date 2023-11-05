# mioti-platforms-j2-awsiot

## Clonar repositorio
```
git clone https://github.com/alvarozornoza/mioti-platforms-j2-azure.git
```

## Crear virtual environment e instalar requirements

### Windows 10

```
cd mioti-platforms-j2-awsiot/simulator
py -m pip install virtualenv
py -m venv ./venv
.\venv\Scripts\activate
py -m pip install -r requirements.txt

deactivate
```

### Linux 
```
cd mioti-platforms-j2-awsiot/simulator
sudo apt-get install python-pip

pip install virtualenv
// sudo apt install virtualenv

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install -r requirements.txt

deactivate
```
