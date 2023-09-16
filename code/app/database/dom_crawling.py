from bs4 import BeautifulSoup
from requests import post
from requests.cookies import RequestsCookieJar

# mongo
from pymongo import MongoClient

# MongoDB 연결 정보
MONGO_URI = ""
MONGO_DB = "markData"
MONGO_COLLECTION = "mark_data"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

c = """
EV   rc8oFfMi6CA6aMrPqkjt+AI8Y5kVN5iOfMEvL6l357k=   .kipris.or.kr   /   Session   46               Medium   
DG_CONFIG   G11111111111111111SX11100110011011110   .kipris.or.kr   /   Session   46               Medium   
JM_CONFIG   G11111111111111SX01111111110010   .kipris.or.kr   /   Session   40               Medium   
KP_CONFIG   4111211177517311151711115111100000000000   .kipris.or.kr   /   Session   49               Medium   
KA_CONFIG   G0000000000000S110111000   .kipris.or.kr   /   Session   33               Medium   
AT_CONFIG   G0000000000000S111110110111   .kipris.or.kr   /   Session   36               Medium   
AB_CONFIG   G11001111111111111111111111110S10000111000111100001000   .kipris.or.kr   /   Session   63               Medium   
NPSUSER   YL60PZGDXLfD0Psncw4UouefTqcbQy10xpKSpxuA3Rc=   .kipris.or.kr   /   Session   51               Medium   
TM_SRCH_HISTORY   2A26D04B01628CBC2D2E920720E16F69E6A673EA6425593C2159F541772D6E08B73D56B044967448FE2FF7DEEA41A0E59DABA421FECF418872C93E759E7E8A9D73135949C02574D98DF06BE0BC19D07260A9090F35D97A064706E3883D1E25E35A4D928F2270874E88C54E38B3F822DA27002DC3EDF2DB40   .kipris.or.kr   /   2024-05-23T01:17:18.924Z   255               Medium   
AD_CONFIG   G11111111111111S1111111111111000   .kipris.or.kr   /   Session   41               Medium   
KPAT_RECENTLY_JOB   1020210100222|1020160034503|1020120086746|1020220159820|1020180000652|1020150099743|1020170010605|1020190157700|1020210112887|1020160152111   .kipris.or.kr   /   2024-04-30T10:47:58.228Z   156               Medium   
USERID   rOzsgjdi7x0JtcBlz345WAjnTL66ejn77LCkvTbiv24=   .kipris.or.kr   /   Session   50               Medium   
_ga_0R1RZQKLPX   GS1.1.1684888492.1.1.1684888618.0.0.0   .kipris.or.kr   /   2024-06-27T00:36:58.535Z   51               Medium   
K2_CONFIG   G1111111111111111111111S111111111000000000   .kipris.or.kr   /   Session   51               Medium   
NKP_CONFIG   G1111111111111111111111S110001000000000000   .kipris.or.kr   /   Session   52               Medium   
JSESSIONID   nRfDXMAretmTixkInfgog83aErGCy9ZALcaShdGOaId51X4mxRDmln1qbmDKgEIj.amV1c19kb21haW4va2R0ajE=   kdtj.kipris.or.kr   /kdtj   Session   99   ✓            Medium   
TM_CONFIG   G11111111111111111SX11111110011111100   .kipris.or.kr   /   Session   46               Medium   
_gid   GA1.3.559972026.1684826518   .kipris.or.kr   /   2023-05-25T01:17:18.000Z   30               Medium   
NAB_CONFIG   G11001111111111111111111111110S10000010000000010000   .kipris.or.kr   /   Session   61               Medium   
JSESSIONID   B1yn4d8rdgruFYGkM1E44enOF73R5VWYLkkaDiNdPbtQXGdix5B3jRa41431R6Hx.amV1c19kb21haW4va2hvbWUx   www.kipris.or.kr   /khome   Session   99   ✓            Medium   
_ga   GA1.3.1529791488.1681896974   .kipris.or.kr   /   2024-06-27T01:17:18.434Z   30               Medium   
TM_RECENTLY_JOB   4120120023215   .kipris.or.kr   /   2024-05-10T09:04:12.776Z   28               Medium   
KPAT_SRCH_HISTORY   D052B21D07EEAD2F98F4D423C298BA907379E49D5414490177986A02D289DE4C40B8055B719E92B00BC5EFACC302EA5306BD83E68D399F286E1CC95434603A6F952807D871B2FE524B060A5CE5BB60AAE256A7D92B839D46C8F68CB372CEFDB113DCD2A0C50467F048D3150B29FD22D0F5617B730D3B8ECBA05D4AD2E2A8852E4E89C2C71764064B42B6492AB3C21357857EFA381A1B29A0DDF026E1506A5D71   .kipris.or.kr   /   2024-04-30T08:44:33.800Z   337               Medium   
"""


kipris_cookie = RequestsCookieJar()
kipris_dict = {}

for row in c.splitlines()[1:]:
    kipris_cookie.set(row.split()[0], row.split()[1])
    kipris_dict[row.split()[0]] = row.split()[1]

url = "http://kdtj.kipris.or.kr/kdtj/grrt1000a.do?method=searchTM"

params = {
    "piSearchYN": "N",
    "queryText": "AD=[20130520~20230520]",
    "searchInResultCk": "undefined",
    "next": "SimpleListTM",
    "expression": "AD=[20130520~20230520]",
    "beforeExpression": "AD=[20130515~20230515]",
    "query": "AD=[20130520~20230520]",
    "rights": "TM",
    "config": "G11111111111111111SX11111110011111100",
    "configChange": "N",
    "searchInTrans": "N",
    "searchInResult": "N",
    "searchInComplate": "N",
    "strstat": "TOP|KW",
    "paging": 0,
    "maxCount": 0,
    "numPageLinks": 10,
    "currentPage": 1,
    "natlCD": "null",
    "docsFound": 0,
    "bookMarkCnt": 0,
    "numPerPage": 150,
    "submitFlag": "N",
    "searchFg": "Y",
    "SEL_PAT": "TM",
    "merchandiseString": "td40,td41,td42,td43,td44,td45,td47,td48,tdmd,",
    "measureString": "R,",
    "patternString": "NAKletter,NAKfigure,NAKlmixed,NAKfmixed,NAKsounds,NAKfragre,TPDcommon,TPDcolors,TPDcolor,TPDdimens,TPDcmixed,TPDdimcol,TPDhologr,TPDaction,TPDvisual,TPDinvisible,",
    "ipMarketDealFlag": 0,
    "searchInTransCk": "undefined",
    "history": "False",
}


# 페이지 수에 따라 반복
currentPage = 454

while True:
    if currentPage == 1001:
        break

    params["currentPage"] = currentPage
    resp = post(url, params=params, data=params, headers=headers, cookies=kipris_dict)
    html_content = resp.text
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.select(".search_section > article")
    print(len(articles))

    if len(articles) < 0:
        break

    for article in articles:
        # 1
        title = article.select_one(".search_section_title > .stitle > a:nth-of-type(2)").get_text()
        if title == "(상표명 정보 없음)":
            title = "NULL"

        # 2
        productCategories = " ".join(
            [
                a.text
                for a in article.select(
                    ".search_basic_info > ul.search_info_list > li:nth-of-type(1) > a"
                )
            ]
        )
        if productCategories == "":
            productCategories = "NULL"

        # 3
        applicantName = article.select_one(
            ".search_basic_info > ul.search_info_list > li:nth-of-type(2) > span:nth-of-type(2)"
        ).get_text()
        if applicantName == "":
            applicantName = "NULL"

        # 4
        applicationNum = "".join(
            filter(
                str.isdigit,
                article.select_one(
                    ".search_basic_info > ul.search_info_list > li:nth-of-type(3)"
                ).get_text(),
            )
        )
        if applicationNum == "":
            applicationNum = "NULL"

        # 5
        applicationDate = (
            article.select_one(".search_basic_info > ul.search_info_list > li:nth-of-type(4)")
            .get_text()
            .split(":")[1]
            .strip()
        )
        if applicationDate == "":
            applicationDate = "NULL"

        # 6
        regNum = (
            article.select_one(".search_basic_info > ul.search_info_list > li:nth-of-type(5)")
            .get_text()
            .split(":")[1]
            .strip()
        )
        if regNum == "":
            regNum = "NULL"

        # 7
        regDate = (
            article.select_one(".search_basic_info > ul.search_info_list > li:nth-of-type(6)")
            .get_text()
            .split(":")[1]
            .strip()
        )
        if regDate == "":
            regDate = "NULL"

        # 8
        publicationNum = "".join(
            filter(
                str.isdigit,
                article.select_one(
                    ".search_basic_info > ul.search_info_list > li:nth-of-type(7)"
                ).get_text(),
            )
        )
        if publicationNum == "":
            publicationNum = "NULL"
        if collection.find_one({"publicationNum": publicationNum}):
            print("Duplicate publicationNum:", publicationNum)
            continue

        # 9
        publicationDate = (
            article.select_one(".search_basic_info > ul.search_info_list > li:nth-of-type(8)")
            .get_text()
            .split(":")[1]
            .strip()
        )
        if publicationDate == "":
            publicationDate = "NULL"

        # 10
        agentName = article.select_one(
            ".search_basic_info > ul.search_info_list > li:nth-of-type(10) > span:nth-of-type(2)"
        ).get_text()
        if agentName == "":
            agentName = "NULL"

        # 11
        regPrivilegeName = (
            article.select_one(
                ".search_basic_info > ul.search_info_list > li:nth-of-type(11) > span:nth-of-type(2)"
            )
            .get_text()
            .strip()
        )
        if regPrivilegeName == "":
            regPrivilegeName = "NULL"
        title = article.select_one(".search_section_title > .stitle > a:nth-of-type(2)").get_text()

        data = {
            "title": title,
            "productCategories": productCategories,
            "applicantName": applicantName,
            "applicationNum": applicationNum,
            "applicationDate": applicationDate,
            "regNum": regNum,
            "regDate": regDate,
            "publicationNum": publicationNum,
            "publicationDate": publicationDate,
            "agentName": agentName,
            "regPrivilegeName": regPrivilegeName,
        }

        result = collection.insert_one(data)
        print("Data inserted successfully. Inserted ID:", result.inserted_id)

    currentPage += 1
    print("——————————", currentPage, "——————————")


# 연결 종료
client.close()
