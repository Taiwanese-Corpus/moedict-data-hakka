# -*- coding: utf-8 -*-
import json
from os.path import dirname, abspath, join
import re
import yaml
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 轉到臺灣言語資料庫.調號處理 import 調號處理
from 轉到臺灣言語資料庫.客話辭典正規化 import 客話辭典正規化
from 轉到臺灣言語資料庫.缺字處理 import 缺字處理
from 轉到臺灣言語資料庫.例詞句判斷種類 import 例詞句判斷種類


class 整合到資料庫:
    專案目錄 = join(dirname(abspath(__file__)), '..')
    _分析器 = 拆文分析器()
    _粗胚 = 文章粗胚()
    _譀鏡 = 物件譀鏡()
    _轉音家私 = 轉物件音家私()

    def 加華語詞目(self):
        for 華語, 腔口資料 in self.整理好詞目格式():
            for 腔口, 漢字, 羅馬字 in 腔口資料:
                if 華語 == '':
                    yield {
                        '語言腔口': 腔口,
                        '種類': '字詞',
                        '文本資料': 漢字,
                        '屬性': {'音標': 羅馬字}
                    }
                else:
                    for 華語詞 in 華語.split('、'):
                        yield {
                            '語言腔口': 腔口,
                            '種類': '字詞',
                            '外語語言': '華語',
                            '外語資料': 華語詞,
                            '下層': [{'文本資料': 漢字, }]
                        }

    def 加例詞句(self):
        例詞句 = 例詞句判斷種類()
        for 客話資料, 華語資料 in self.整理好釋義格式():
            種類 = 例詞句.判斷種類(客話資料, 華語資料)
            if 華語資料 is None:
                yield {
                    '種類': 種類,
                    '語言腔口': '四縣腔',
                    '文本資料': 客話資料,
                }
            else:
                yield {
                    '種類': 種類,
                    '語言腔口': '四縣腔',
                    '外語語言': '華語',
                    '外語資料': 華語資料,
                    '下層': [{'文本資料': 客話資料, }]
                }

    def 資料抓出來(self):
        with open(join(self.專案目錄, 'wip.json')) as 檔案:
            for 一筆資料 in json.load(檔案):
                if len(一筆資料) == 1:
                    '只有檔名，空的資料'
                    continue
                yield 一筆資料

    _缺字處理 = 缺字處理()

    def 整理好詞目格式(self):
        編號解析 = re.compile('(\d+)')
        漢字解析 = re.compile('【(.+)】')
        for 資料 in self.資料抓出來():
            編號 = 編號解析.search(資料['檔名']).group(1)
#             print(編號)
            華語 = 資料['對應華語'].strip()
            漢字 = self._缺字處理.取代(
                漢字解析.match(資料['詞目'].strip()).group(1)
            )
            腔口資料 = []
            for 音欄位 in [
                '四縣音', '南四縣', '海陸音',
                '大埔音', '饒平音', '詔安音',
            ]:
                音標 = 資料[音欄位].strip()
                if 音標 != '':
                    腔口 = 音欄位.rstrip('音') + '腔'
                    try:
                        處理後漢字, 處理後音標 = self.處理腔口資料(腔口, 漢字, 音標)
                        腔口資料.append(
                            (腔口, 處理後漢字, 處理後音標)
                        )
                    except Exception as 錯誤:
                        print(錯誤)
                        print(編號, 腔口, 漢字, 音標, 華語)
            yield 華語, 腔口資料

    def 整理好釋義格式(self):
        客話解析 = re.compile('\ufff9(.+)')
        華語解析 = re.compile('\ufffb（(.+)）')
        解說解析 = re.compile('﹝.*?﹞')
        拿掉解說 = lambda 字串: 解說解析.sub('', 字串)
        詞變化解析 = re.compile('（(.*?)）')
        拿掉詞變化括號 = lambda 字串: 詞變化解析.sub(lambda 物件: 物件.group(1), 字串)
        for 資料 in self.資料抓出來():
            for 解釋 in 資料['釋義']:
                try:
                    for 客話例, 華語翻譯 in 解釋['example']:
                        客話資料 = 拿掉詞變化括號(
                            拿掉解說(
                                self._缺字處理.取代(
                                    客話解析.match(客話例).group(1)
                                )
                            )
                        )
                        try:
                            華語資料 = 拿掉解說(
                                華語解析.match(華語翻譯).group(1)
                            )
                        except AttributeError:
                            華語資料 = None
                        if 客話資料 != '。':
                            yield 客話資料, 華語資料
                except KeyError:
                    pass

    def 處理腔口資料(self, 腔口, 漢字, 音標):
        無字音標 = self._正規化.處理音標頭前字(音標)
        加分字音標 = self._粗胚.數字英文中央全加分字符號(無字音標)
        調整後漢字, 調整後音標 = self._正規化.調整方言的詞條(漢字, 加分字音標)
        調號音標 = self._調號.數字轉調號(調整後音標, 腔口)
        return self.漢字音標配對(調整後漢字, 調號音標)

    _正規化 = 客話辭典正規化()
    _調號 = 調號處理()

    def 漢字音標配對(self, 漢字, 音標):
        處理了音標 = self._粗胚.符號邊仔加空白(音標)
        原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
        return self._譀鏡.看型(原音章物件), self._譀鏡.看音(原音章物件)


if __name__ == '__main__':
    公家資料 = {
        '來源': {'名': '臺灣客家語常用詞辭典網路版'},
        '版權': '標註出處、不可改作、不可作商業利用',
        '著作所在地': '臺灣',
        '著作年': '2006',
    }
    到資料庫 = 整合到資料庫()
    下層 = []
    for 資料 in 到資料庫.加華語詞目():
        下層.append(資料)
    for 資料 in 到資料庫.加例詞句():
        下層.append(資料)
    公家資料['下層'] = 下層
    with open('臺灣客家語常用詞辭典網路版語料.yaml', 'w') as 檔案:
        yaml.dump(公家資料, 檔案, default_flow_style=False, allow_unicode=True)
