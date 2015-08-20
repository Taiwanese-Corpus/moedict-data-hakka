# 轉到臺灣言語資料庫

## 流程

## 匯入資料庫
在`臺灣言語資料庫`專案目錄下
```bash
git clone https://github.com/Taiwanese-Corpus/moedict-data-hakka.git
sudo apt-get install -y python3 python-virtualenv
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
echo "from 轉到臺灣言語資料庫.整合到資料庫 import 走 ; 走()" | PYTHONPATH=moedict-data-hakka python manage.py shell
```

## 開發試驗
在`moedict-data-hakka`專案目錄下
```
sudo apt-get install -y python-virtualenv g++ libxml2-dev libxslt-dev python-dev
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r 轉到臺灣言語資料庫/requirements.txt
python -m unittest 
```

