from 臺灣言語工具.基本元素.公用變數 import 標點符號


class 例詞句判斷種類:

    def 判斷種類(self, 客, 華):
        if 華 is None:
            return '字詞'
        if '、' in 客:
            return '字詞'
        if 客[-1] in 標點符號:
            return '語句'
        if len(客) <= 6:
            return '字詞'
        return '語句'
