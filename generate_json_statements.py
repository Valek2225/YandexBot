from json import dump

dict_json = {}
from main import types, stages, years, days, problems

for t in types:
    dict_json[t] = {'problems': '.'}
    for s in stages:
        dict_json[t][s] = {'problems': '.'}
        for y in years:
            dict_json[t][s][y] = {'problems': '.'}
            for d in days:
                dict_json[t][s][y][d] = {'problems': '.'}
                for p in problems:
                    dict_json[t][s][y][d][p] = {'problems': '.'}

# 2009-2010
dict_json['VSOSH']['Regional_stage']['2009'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2009-2010/region_tasks/Informatics/tasks-iikt-9-11-reg-09-0.pdf'
dict_json['VSOSH']['Final_stage']['2009'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2009-2010/final_tasks/new-cut/iikt/tasks-iikt-9-11-final-2009-10.pdf'
# 2010-2011
dict_json['VSOSH']['Regional_stage']['2010'][
    'problems'] = 'https://olimpiada.ru/upload/files/Arhive_tasks/2010-2011/region_tasks/Informatics/tasks-iikt-9-11-reg-10-1.pdf'
dict_json['VSOSH']['Final_stage']['2010'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2010-2011/final_tasks/iikt/tasks-iikt-9-11-final-10-1.pdf'
# 2011-2012
dict_json['VSOSH']['Regional_stage']['2011'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2011-2012/region_tasks/Informatics/tasks-iikt-9-11-reg-11-2.pdf'
dict_json['VSOSH']['Final_stage']['2011'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2011-2012/final_tasks/iikt/tasks-iikt-9-11-final-11-2.pdf'
# 2012-2013
dict_json['VSOSH']['Regional_stage']['2012'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2012-13/reg/iikt/tasks-iikt-9-11-reg-12-3.pdf'
dict_json['VSOSH']['Final_stage']['2012'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2012-13/final/iikt/tasks-iikt-9-11-final-12-3.pdf'
# 2013-2014
dict_json['VSOSH']['Regional_stage']['2013'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2013-14/region_tasks/iikt/tasks-iikt-9-11-reg-13-4.pdf'
dict_json['VSOSH']['Final_stage']['2013'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2013-14/final%20tasks/iikt/tasks-iikt-9-11-final-13-4.pdf'
# 2014-2015
dict_json['VSOSH']['Regional_stage']['2014'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2014-15/region_tasks/iikt/tasks-iikt-9-11-reg-14-5.pdf'
dict_json['VSOSH']['Final_stage']['2014'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2014-15/final_tasks/iikt/tasks-iikt-9-11-final-14-5.pdf'
# 2015-2016
dict_json['VSOSH']['Regional_stage']['2015'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2015-16/region/iikt/tasks-iikt-9-11-reg-15-6.pdf'
dict_json['VSOSH']['Final_stage']['2015'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2015-16/final/iikt/tasks-iikt-9-11-final-15-6.pdf'
# 2016-2017
dict_json['VSOSH']['Regional_stage']['2016'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2016-17/region/iikt/tasks-iikt-9-11-reg-16-7.pdf'
dict_json['VSOSH']['Final_stage']['2016'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2016-17/final/iikt/task-iikt-9-11-final-16-7.pdf'
# 2017-2018
dict_json['VSOSH']['Regional_stage']['2017'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2017-18/region/iikt/tasks-iikt-9-11-reg-17-8.pdf'
dict_json['VSOSH']['Final_stage']['2017'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2017-18/final/iikt/73-ans-iikt-9-11-final-17-8.pdf'
# 2018-2019
dict_json['VSOSH']['Regional_stage']['2018'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2018-19/region/iikt/task-iikt-9-11-reg-18-9.pdf'
dict_json['VSOSH']['Final_stage']['2018'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2018-19/final/iikt/73-tasks-iikt-9-11-final-18-9.pdf'
# 2019-2020
dict_json['VSOSH']['Regional_stage']['2019'][
    'problems'] = 'https://vos.olimpiada.ru/upload/files/Arhive_tasks/2019-20/region/iikt/tasks-iikt-9-11-reg-19-20.pdf'
dict_json['VSOSH']['Final_stage']['2019'][
    'problems'] = '.'
fl = open('statements.json', 'w')
dump(dict_json, fl)
fl.close()
