# 轉到臺灣言語資料庫

## 匯入
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/moedict-data-hakka/臺灣客家語常用詞辭典網路版語料.yaml
```

## 產生資料庫格式
```bash
git clone https://github.com/Taiwanese-Corpus/moedict-data-hakka.git
sudo apt-get install -y python3 python-virtualenv libyaml-dev
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python 轉到臺灣言語資料庫/整合到資料庫.py
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
