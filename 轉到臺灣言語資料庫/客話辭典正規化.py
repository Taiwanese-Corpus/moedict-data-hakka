# -*- coding: utf-8 -*-


class 客話辭典正規化:

    def 處理音標頭前字(self, 音標):
        音標 = 音標.split('）')[-1]
        音標 = 音標.replace('文', '')
        音標 = 音標.replace('白', '')
        return 音標.strip()

    def 調整錯誤的詞條(self, 詞目, 新音):
        if 新音 in self.換音:
            #             							print('{0}\n{1}\n{2}\n音標改正：{3}'.
            #             								format(編號, 詞目, 新音, 換音[新音]))
            新音 = self.換音[新音]
            新詞目 = 詞目
        elif 詞目 == '毆畀死' and 新音 == 'eu55-bun11-gi55-si53':  # 饒平音無合音
            新詞目 = '毆分佢死'
        elif (詞目, 新音.replace('-', ' ')) in self.海陸表:
            新詞目 = self.海陸表[(詞目, 新音.replace('-', ' '))]
        else:
            新詞目 = 詞目
        新音 = 新音.replace('9', '31')
        return 新詞目, 新音
    海陸表 = {
        ('時錶仔', 'shi55 biau24'): '時錶',
        ('磨刀仔', 'no55 do53'): '磨刀',
        ('紙炮仔', 'zhi24 pau11'): '紙炮',
        ('竹馬仔', 'zhug5 ma53'): '竹馬',
        ('魚脯仔', 'ng55 pu24'): '魚脯',
        ('做粄仔', 'zo11 ban24'): '做粄',
        ('嫩葉仔', 'nun33 rhab2'): '嫩葉',
        ('茶壺仔', 'ca55 fu55'): '茶壺',
        ('嬰兒仔', 'o53 nga11'): '嬰兒',
        ('梅仔樹', 'moi55 shu33'): '梅樹',
        ('種痘仔', 'zhung11 teu33'): '種痘',
        ('送鬼仔', 'sung11 gui24'): '送鬼',
        ('頭臥臥仔', 'teu55 ngo11 ngo11'): '頭臥臥',
        ('時鐘仔', 'shi55 zhung53'): '時鐘'
    }
    換音 = {'han113 fa53 rhid21 tai53 doi33 zhin53 gin33 mo113 rhid21 pied54':
          'han113 fa53 rhid21 tai53 doi33, zhin53 gin33 mo113 rhid21 pied54',
          'mang11 shid5 ng53 ngied5 zied2 zung53 o53 po55 m55 ho53 ngib5 vung53':
          'mang11 shid5 ng53 ngied5 zied2 zung53, o53 po55 m55 ho53 ngib5 vung53',
          'cai55 ga11 cien11 ngid24 hoo31 chid24 mun53 ban31 zhio11 nan53':
          'cai55 ga11 cien11 ngid24 hoo31, chid24 mun53 ban31 zhio11 nan53',
          'teu55 na55 cab2 vo55 chan53 liau55 diau11':
          'teu55 na55 cab2 vo55 chan53 －－ liau55 diau11',
          'uai33 zhoi53 choi33 lab54 ba31，rhid21 ton113 sia113 ki53':
          'uai33 zhoi53 choi33 lab54 ba31 －－ rhid21 ton113 sia113 ki53',
          'gung33 bud21 li113 po113 chin53 bud21 li113 to113':
          'gung33 bud21 li113 po113, chin53 bud21 li113 to113',
          'ho53 ma11 m55 shid5 shid5 fui55 teu55 co53':
          'ho53 ma11 m55 shid5 fui55 teu55 co53',
          'han113 fa53 rhid21 tai53 doi33 zhin53 gin33 mo113 rhid21 pied54':
          'han113 fa53 rhid21 tai53 doi33, zhin53 gin33 mo113 rhid21 pied54',
          }
