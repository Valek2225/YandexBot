from json import dump, load
from main import types, stages, years, days, problems
from config import LOGIN, PASSWORD
import requests
from lxml import html

file_id = open('statements.json', 'r')
statements_file = load(file_id)
file_id.close()
session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
loginPageResp = session.get("https://informatics.msk.ru/login/index.php", stream=True)

loginPageResp.raise_for_status()
loginPageResp.raw.decode_content = True

parser = html.parse(loginPageResp.raw)

loginToken = parser.xpath("//form[@class='mt-3' and @id='login']/input[@name='logintoken']/@value")
login_anchor = parser.xpath("//form[@class='mt-3' and @id='login']/input[@name='anchor']/@value")
if not loginToken: raise ValueError("Field 'logintoken' was not found")

loginTokenVal = loginToken[0]
loginAnchorVal = login_anchor[0]

loginResp = session.post(
    "https://informatics.msk.ru/login/index.php",
    data={
        'anchor': loginAnchorVal,
        "logintoken": loginTokenVal,
        "username": LOGIN,
        "password": PASSWORD
    }
)
reg = {}
for i in range(2009, 2020):
    reg[i] = {1: {'A': -1,
                  'B': -1,
                  'C': -1,
                  'D': -1},
              2: {'A': -1,
                  'B': -1,
                  'C': -1,
                  'D': -1}
              }
roi = {}
for i in range(2009, 2019):
    roi[i] = {1: {'A': -1,
                  'B': -1,
                  'C': -1,
                  'D': -1},
              2: {'A': -1,
                  'B': -1,
                  'C': -1,
                  'D': -1}
              }
startValueReg = {}
startValueReg[2009] = [1205, 1209]
startValueReg[2010] = [1922, 1926]
startValueReg[2011] = [3206, 3181]
startValueReg[2012] = [3864, 3868]
startValueReg[2013] = [111488, 111488]
startValueReg[2014] = [112036, 112040]
startValueReg[2015] = [112744, 112748]
startValueReg[2016] = [113096, 113096]
startValueReg[2017] = [113439, 113443]
startValueReg[2018] = [113757, 113761]
startValueReg[2019] = [114038, 114042]
startValueRoi = {}
startValueRoi[2009] = [1337, 1340]
startValueRoi[2010] = [2529, 2532]
startValueRoi[2011] = [3393, 3397]
startValueRoi[2012] = [111221, 111221]
startValueRoi[2013] = [111633, 111637]
startValueRoi[2014] = [112335, 112328]
startValueRoi[2015] = [112815, 112819]
startValueRoi[2016] = [113217, 113221]
startValueRoi[2017] = [113544, 113548]
startValueRoi[2018] = [113911, 113915]
for i in range(2009, 2020):
    for j in range(8):
        if j >= 4:
            reg[i][2][problems[j % 4]] = startValueReg[i][1] + j % 4
        else:
            reg[i][1][problems[j]] = startValueReg[i][0] + j

for i in range(2009, 2019):
    for j in range(8):
        if j >= 4:
            roi[i][2][problems[j % 4]] = startValueRoi[i][1] + j % 4
        else:
            roi[i][1][problems[j]] = startValueRoi[i][0] + j
roi[2009][1]['D'] = -1
roi[2009][2]['D'] = -1
roi[2010][1]['D'] = -1
roi[2010][2]['D'] = -1
roi[2014][2]['D'] = -1
roi[2014][1]['A'] = 112335
roi[2014][1]['B'] = 112332
roi[2014][1]['C'] = 112333
roi[2014][1]['D'] = 112334
roi[2013][2]['B'] = 111644
roi[2013][2]['C'] = 111645
roi[2013][2]['D'] = 111646
roi[2012][2]['C'] = 111562
roi[2012][2]['D'] = 111227
fl = open('problems.json', 'w')
informatics = [str(x) for x in range(2009, 2020)]
dict_json = {}
for t in types:
    dict_json[t] = {}
    for s in stages:
        dict_json[t][s] = {}
        for y in years:
            dict_json[t][s][y] = {}
            for d in days:
                dict_json[t][s][y][d] = {}
                for p in problems:
                    plat = 'cf'
                    if y in informatics:
                        plat = 'inf'
                    id_problem = -1
                    if s == 'Regional_stage':
                        id_problem = reg[int(y)][int(d)][p]
                    else:
                        try:
                            id_problem = roi[int(y)][int(d)][p]
                        except:
                            id_problem = -1
                    name = 'unknown'
                    if id_problem != -1:
                        url = (
                            f"https://informatics.msk.ru/py/problem/{id_problem}/filter-runs?problem_id={id_problem}&from_timestamp=-1&to_timestamp=-1&"
                            "user_id=854350&lang_id=-1&status_id=-1&statement_id=0&count=10&with_comment=&page=1&group_id=0&course_id=0")
                        subResp = session.get(url)
                        r = subResp.json()
                        try:
                            name = r['data'][0]['problem']['name']
                        except:
                            print(r)
                    st = '.'
                    try:
                        st = statements_file[t][s][str(int(y) - 1)]['problems']
                    except:
                        st = '.'
                    dict_json[t][s][y][d][p] = {'id': id_problem,
                                                'platform': plat,
                                                'name': name,
                                                'statement': st
                                                }
dump(dict_json, fl)
fl.close()
