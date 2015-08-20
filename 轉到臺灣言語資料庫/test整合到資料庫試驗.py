from unittest.case import TestCase
from 轉到臺灣言語資料庫.例詞句判斷種類 import 例詞句判斷種類


class 整合到資料庫試驗(TestCase):

    def test_無華語(self):
        self.檢查種類(
            ('戲班、資優班。', None),
            '字詞'
        )

    def test_短閣無標點(self):
        self.檢查種類(
            ('恁樣仔个人', '這樣子的人'),
            '字詞'
        )

    def test_短閣有標點(self):
        self.檢查種類(
            ('粥恁鮮。', '稀飯這麼稀。'),
            '語句'
        )

    def test_長閣無標點有頓號(self):
        self.檢查種類(
            ('圓球、圓桌仔', '圓桌'),
            '字詞'
        )

    def test_長閣有標點(self):
        self.檢查種類(
            ('做你盡步來。', '你儘管把招數使出來吧。'),
            '語句'
        )
        
    def test_長閣無標點無頓號(self):
        self.檢查種類(
            ('這條海參蝓膏汁帶，拿毋核', '這條海參黏滑滑的，拿不牢'),
            '語句'
        )

         


    def 檢查種類(self, 語料, 結果):
        例詞句 = 例詞句判斷種類()
        self.assertEqual(
            例詞句.判斷種類(
                *語料
            ),
            結果
        )
