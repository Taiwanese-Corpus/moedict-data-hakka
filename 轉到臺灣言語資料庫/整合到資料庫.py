# -*- coding: utf-8 -*-
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from csv import DictReader
import json
from os.path import dirname, abspath, join
import re
from 臺灣言語工具.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 轉到臺灣言語資料庫.調號處理 import 調號處理
from 轉到臺灣言語資料庫.客話辭典正規化 import 客話辭典正規化
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 轉到臺灣言語資料庫.缺字處理 import 缺字處理


class 整合到資料庫:
    臺灣客家語常用詞辭典網路版 = 來源表.objects.get_or_create(名='臺灣客家語常用詞辭典網路版')[0]
    薛丞宏 = 來源表.objects.get_or_create(名='薛丞宏')[0]
    版權 = 版權表.objects.get_or_create(版權='標註出處、不可改作、不可作商業利用')[0]
    專案目錄 = join(dirname(abspath(__file__)), '..')
    公家內容 = {
        '來源': 臺灣客家語常用詞辭典網路版,
        '版權': 版權,
        '語言腔口': '閩南語',
        '著作所在地': '臺灣',
        '著作年': '2006',
    }
    _分析器 = 拆文分析器()
    _粗胚 = 文章粗胚()
    _譀鏡 = 物件譀鏡()
    _轉音家私 = 轉物件音家私()

    def 處理詞條(self, 詞條, 收錄者):
        公家內容 = {
            '收錄者': 收錄者,
        }
        公家內容.update(self.公家內容)

#         '種類': '字詞',
        for 華語 in 詞條['華語對譯'].strip(';').split(';'):
            華語內容 = {
                '外語語言': '華語',
                '外語資料': 華語.strip(),
            }
            華語內容.update(公家內容)
            外語 = 外語表.加資料(華語內容)
#             外語 = None
            self.加臺語詞條(公家內容, 詞條['ID'], 外語, 詞條['台語漢字'], 詞條['台語羅馬字'])
            if 詞條['台語羅馬字2'].strip() != '':
                self.加臺語詞條(公家內容, 詞條['ID'], 外語, 詞條['台語漢字'], 詞條['台語羅馬字2'])

    def 加臺語詞條(self, 公家內容, 編號, 外語, 漢字, 羅馬字):
        try:
            處理減號漢字 = self._粗胚.建立物件語句前處理減號(教會羅馬字音標, 漢字)
            處理了漢字 = self._粗胚.符號邊仔加空白(處理減號漢字)
            處理減號音標 = self._粗胚.建立物件語句前處理減號(教會羅馬字音標, 羅馬字)
            處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
            原音章物件 = self._分析器.產生對齊章(處理了漢字, 處理了音標)
            上尾章物件 = self._轉音家私.轉音(教會羅馬字音標, 原音章物件)
            型 = self._譀鏡.看型(上尾章物件)
            音 = self._譀鏡.看音(上尾章物件)
        except Exception as 錯誤:
            print(編號, 錯誤)
            型 = 漢字
            音 = 羅馬字

        臺語內容 = {
            '文本資料': 型.strip(),
            '屬性': {'音標': 音.strip()}
        }
        臺語內容.update(公家內容)
        外語.翻母語(臺語內容)

    def 檢查資料有改過無(self):
        原始檔名 = join(self.專案目錄, '原始資料', 'Taihoa.csv')
        全部原始資料 = {}
        with open(原始檔名) as 原始檔案:
            for 一筆 in DictReader(原始檔案):
                全部原始資料[一筆['ID']] = 一筆
        for 一筆 in self.掠編輯過資料出來():
            原始資料 = 全部原始資料[一筆['ID']]
            for 欄位, 內容 in 一筆.items():
                if 欄位 in ['']:
                    if 內容.strip() not in ['', r'\\']:
                        raise RuntimeError('空欄位有資料：{}'.format(內容.strip()))
                    continue
                if 內容 != 原始資料[欄位]:
                    raise RuntimeError(
                        '資料有校對過，請看一下：{}、{}、{}、{}'.format(
                            欄位, 一筆['ID'], 原始資料[欄位], 內容
                        )
                    )

    def 資料抓出來(self):
        with open(join(self.專案目錄, 'wip.json')) as 檔案:
            for 一筆資料 in json.load(檔案):
                if len(一筆資料) == 1:
                    '只有檔名，空的資料'
                    continue
                yield 一筆資料

    _缺字處理 = 缺字處理()

    def 整理好格式(self):
        編號解析 = re.compile('(\d+)')
        漢字解析 = re.compile('【(.+)】')
        for 資料 in self.資料抓出來():
            編號 = 編號解析.search(資料['檔名']).group(1)
#             print(編號)
            華語 = 資料['對應華語'].strip().split('、')
            漢字 = self._缺字處理.取代(
                漢字解析.match(資料['詞目'].strip()).group(1)
            )

            for 音欄位 in [
                '四縣音', '南四縣', '海陸音',
                '大埔音', '饒平音', '詔安音',
            ]:
                音標 = 資料[音欄位].strip()
                if 音標 != '':
                    腔口 = 音欄位.rstrip('音') + '腔'
                    try:
                        self.處理腔口資料(腔口, 漢字, 音標)
                    except Exception as 錯誤:
                        print(錯誤)
                        print(編號, 腔口, 漢字, 音標, 華語)

#                 break
        "                print(一筆資料['釋義'])有例句"

    def 處理腔口資料(self, 腔口, 漢字, 音標):
        無字音標 = self._正規化.處理音標頭前字(音標)
        加分字音標 = self._粗胚.數字英文中央全加分字符號(無字音標)
        調整後漢字, 調整後音標 = self._正規化.調整錯誤的詞條(漢字, 加分字音標)
        調號音標 = self._調號.數字轉調號(調整後音標, 腔口)
        return self.漢字音標配對(調整後漢字, 調號音標)

    _正規化 = 客話辭典正規化()
    _調號 = 調號處理()

#     def 音標處理(self, 腔口, 漢字, 音標):
#         return 調號音標

    def 漢字音標配對(self, 漢字, 音標):
        處理了音標 = self._粗胚.符號邊仔加空白(音標)
        原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
        return self._譀鏡.看型(原音章物件), self._譀鏡.看音(原音章物件)


def 走(收錄者=整合到資料庫.薛丞宏):
    到資料庫 = 整合到資料庫()
    到資料庫.整理好格式()
    return
    for _第幾个, 詞條 in enumerate(到資料庫.掠編輯過資料出來()):
        try:
            到資料庫.處理詞條(詞條, 收錄者)
        except Exception as e:
            print(詞條, e)
            raise
