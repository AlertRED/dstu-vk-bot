import requests
from lxml import html

headers = {
    'authority': 'edu.donstu.ru',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'origin': 'https://edu.donstu.ru',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'none',
    'referer': 'https://edu.donstu.ru/Rasp/Rasp.aspx?group=32342&sem=1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
    'cookie': '_ga=GA1.2.1873524620.1564039250; _ym_uid=1564039250480631114; _ym_d=1564039250; rasp_default_aspx_ctl00_MainContent_ASPxPageControl1_gvPrep=page1%7cconditions2%7c0%7c3%7c1%7c3%7chierarchy2%7c0%7c-1%7c1%7c-1%7cvisible2%7ct1%7ct0%7cwidth2%7c30%25%7ce; rasp_default_aspx_ctl00_MainContent_ASPxPageControl1_grAud=page1%7cconditions1%7c0%7c3%7chierarchy1%7c0%7c-1%7cvisible1%7ct1%7cwidth1%7c100%25; BITRIX_SM_GUEST_ID=18679913; BITRIX_SM_LAST_VISIT=14.08.2019+20%3A37%3A28; rasp_default_aspx_ctl00_MainContent_ASPxPageControl1=0; rasp_default_aspx_ctl00_MainContent_ASPxPageControl1_grGroup=page1%7cfilter26%7cContains(%5bRaspURL%5d%2c+%27%d0%b2%d0%bf%d1%80%27)%7cconditions1%7c0%7c3%7chierarchy4%7c0%7c-1%7c1%7c-1%7c2%7c-1%7c3%7c-1%7cvisible4%7ct1%7ct2%7ct3%7ct4%7cwidth4%7ce%7ce%7ce%7c50px; ASP.NET_SessionId=bs4if40vwnnfaqlfyinvznp2; __AntiXsrfToken=8877277adbcd48f2a3e045dd8788380d',
}

params = (
    ('group', '32342'),
    ('sem', '1'),
)

data = {
  '__EVENTTARGET': 'ctl00$MainContent$cmbTypeView',
  '__EVENTARGUMENT': '',
  '__VIEWSTATE': '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Ah4LUG9zdEJhY2tVcmwFH1Jhc3BGdWxsLmFzcHg/Z3JvdXA9MzIzNDImc2VtPTFkZAIBD2QWAgIBDw8WAh8CBQoyMS4wOS4yMDE5ZGQCBQ88KwAmBAAPFgQeDEtleUZpZWxkTmFtZQUG0JrQvtC0HwVnZAYPZBAWB2YCAQICAgMCBAIFAgYWBzwrAAwCABYEHg9Db2xWaXNpYmxlSW5kZXgCAx4LR2xvYmFsSW5kZXhmCzwrAAUBABYGHgpHcm91cEluZGV4Zh4JU29ydEluZGV4Zh4JU29ydE9yZGVyCyl6RGV2RXhwcmVzcy5EYXRhLkNvbHVtblNvcnRPcmRlciwgRGV2RXhwcmVzcy5EYXRhLnYxOC4xLCBWZXJzaW9uPTE4LjEuNC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI4OGQxNzU0ZDcwMGU0OWEBPCsADAEAFgIfDgIBPCsADAEAFgIfDgICPCsADAEAFgIfDgIDPCsADAEAFgIfDgIEPCsADAEAFgIfDgIFPCsADAEAFgQeCkNvbFZpc2libGVoHw4CBg8WBwIBAgECAQIBAgICAgIBFgIFf0RldkV4cHJlc3MuV2ViLkdyaWRWaWV3RGF0YVRleHRDb2x1bW4sIERldkV4cHJlc3MuV2ViLnYxOC4xLCBWZXJzaW9uPTE4LjEuNC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI4OGQxNzU0ZDcwMGU0OWEFf0RldkV4cHJlc3MuV2ViLkdyaWRWaWV3RGF0YU1lbW9Db2x1bW4sIERldkV4cHJlc3MuV2ViLnYxOC4xLCBWZXJzaW9uPTE4LjEuNC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI4OGQxNzU0ZDcwMGU0OWETFCsAAxYCHghGaWxlTmFtZQU20KDQsNGB0L/QuNGB0LDQvdC40LUg0LPRgNGD0L/Qv9GLICjQktCf0KA0MSwyMDE5LTIwMjApZGQYPCsABwEFFCsAAmRkZAIpDxYCHwBoZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUbY3RsMDAkTWFpbkNvbnRlbnQkY2JTZW0kREREBR1jdGwwMCRNYWluQ29udGVudCRjYldlZWtzJERERAUhY3RsMDAkTWFpbkNvbnRlbnQkY21iVHlwZVZpZXckREREBRpjdGwwMCRNYWluQ29udGVudCRiQWx0UmFzcAUfY3RsMDAkTWFpbkNvbnRlbnQkQVNQeEdyaWRWaWV3MQUpY3RsMDAkTWFpbkNvbnRlbnQkQVNQeEdyaWRWaWV3MSREWENUTWVudTDpHyNModiE40kCBPLx0b0PtBdlsFUseydIpUZEO4u4Gg==',
  '__VIEWSTATEGENERATOR': 'BE51B940',
  '__PREVIOUSPAGE': 'G6wHIYEVPgYO9A2Arb5Lv2fbjQ9MGvoCmMaG3E2aJNp2zGaFHyJOtQqMgIROl8IF9tDn6nAd5AK63bSm_0wSVzyA_VpdARpBAtaUKjkdeFQ1',
  '__EVENTVALIDATION': '/wEdAAJHOUWDX58Vft3iy1dtqMJLbwysKL6p/id/u1FoeFMDsWie0+bn2Z2jY0XvKFANQdvTgopvAq/raWJgdYQG6RIn',
  'ctl00_MainContent_cbSem_VI': '1',
    'ctl00$MainContent$cbSem': 'Осенний',
  'ctl00$MainContent$cbSem$DDDState': '{&quot;windowsState&quot;:&quot;0:0:-1:0:0:0:-10000:-10000:1:0:0:0&quot;}',
  'ctl00$MainContent$cbSem$DDD$L': '1',
  'ctl00_MainContent_cbWeeks_VI': '3-20',
     'ctl00$MainContent$cmbTypeView': 'Все+недели',

  'ctl00$MainContent$cbWeeks': '3-20',
  'ctl00$MainContent$cbWeeks$DDDState': '{&quot;windowsState&quot;:&quot;0:0:-1:0:0:0:-10000:-10000:1:0:0:0&quot;}',
  'ctl00$MainContent$cbWeeks$DDD$L': '3-20',
  'ctl00_MainContent_cmbTypeView_VI': '0',
  'ctl00$MainContent$cmbTypeView$DDDState': '{&quot;windowsState&quot;:&quot;1:1:12000:485:88:1:298:136:1:0:0:0&quot;}',
  'ctl00$MainContent$cmbTypeView$DDD$L': '0',
  'ctl00$MainContent$ASPxGridView1': '{&quot;keys&quot;:[&quot;/^DXN&quot;,&quot;19076577&quot;,&quot;19076578&quot;,&quot;19076580&quot;,&quot;/^DXN&quot;,&quot;19076584&quot;,&quot;19076586&quot;,&quot;19076587&quot;,&quot;/^DXN&quot;,&quot;19076589&quot;,&quot;19076590&quot;,&quot;/^DXN&quot;,&quot;19076595&quot;,&quot;19076597&quot;,&quot;19076598&quot;,&quot;19076599&quot;],&quot;groupLevelState&quot;:{&quot;0&quot;:[[0,0],[4,4],[8,8],[11,11]]},&quot;callbackState&quot;:&quot;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&quot;,&quot;mergedCellState&quot;:{&quot;0&quot;:[[1,3],[5,7],[9,10],[12,15]]},&quot;selection&quot;:&quot;&quot;,&quot;toolbar&quot;:null}',
  'ctl00$MainContent$ASPxGridView1$DXCTMenu0': '{&quot;selectedItemIndexPath&quot;:&quot;&quot;,&quot;checkedState&quot;:&quot;&quot;}',
  'DXScript': '1_16,1_17,1_28,1_66,1_18,1_19,1_225,1_226,1_26,1_27,1_231,1_20,1_22,1_228,1_234,1_44,1_224,1_24,1_254,1_265,1_266,1_252,1_268,1_276,1_278,1_279,1_274,1_280,1_29,1_36,1_291',
  'DXCss': '1_251,0_1775,1_69,1_70,1_71,1_250,0_1780,0_1884,0_1889,0_1785,0_1790,../dgtu.ico,../css/Bootstrap/bootstrap.css,../css/Bootstrap/bootstrap.offcanvas.css,/css/Mail/plugins/font-awesome/css/font-awesome.min.css?t=1,/css/Stud.css?t=7,/css/common.css?t=2,/css/Rasp/Rasp.css'
}

response = requests.post('https://edu.donstu.ru/Rasp/Rasp.aspx', headers=headers, params=params, data=data)

# print(response.text)

# Записать html в файл
f = open('exemple_html.txt', 'w')
f.write(response.text)

f = open('exemple_html.txt', 'r')

tree = html.fromstring(f.read())
date = tree.xpath('//span[@id="ctl00_MainContent_lbCurYear"]')
date = date[0] if len(date) > 0 else None
group = tree.xpath('//a[@id="ctl00_MainContent_hpGroup"]')
group = group[0] if len(group) > 0 else None
type_schedule = tree.xpath('//input[@id="ctl00_MainContent_cmbTypeView_I"]')
type_schedule = type_schedule[0] if len(type_schedule) > 0 else None
print(date.text)
print(group.text)
print(type_schedule.value)

index = 0
rasp = {}
while True:
    day = tree.xpath('//tr[@id="ctl00_MainContent_ASPxGridView1_DXGroupRowExp' + str(index) + '"]')
    if len(day) > 0:
        print(len(day[0].text), index)
        # # rasp[day[0].text] = {}
        # while True:
        #     item = tree.xpath('//tr[@id="ctl00_MainContent_ASPxGridView1_DXDataRow' + str(index) + '"]')
        #     if len(item)>0:
        #         time = item.xpath('//tr[@class="dx-nowrap dxgv"]')[0].text
        #         print(time)
        #         # rasp[day[0].text][time] =
        #         index += 1
        #     else:
        #         break
    else:
        if index > 30:
            break

    index += 1
