import numpy
import pandas as pd

from SSPRepository import SSPRepository

## ele pega os dados de 2 em dois anos, entaão pega 2010 junto com 2011, 2012 junto com 2013 ....
years = [2011, 2013, 2015, 2017]

FULL_MONTHS = {'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
               'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
               'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'}
natures = [
    {'nature': '[Natureza].[CRIMES CONTRA O PATRIMÔNIO].[CPB ART. 157 CAPUT: ROUBO].[ROUBO A TRANSEUNTE]', 'as': '157'}]

locations = [
    {'location': 'AISP 01 - ÁREA CENTRAL DE GOIÂNIA', 'as': 1},
    {'location': 'AISP 02 - ÁREA NOROESTE DE GOIÂNIA', 'as': 2},
    {'location': 'AISP 03 - ÁREA NORTE DE GOIÂNIA', 'as': 3},
    {'location': 'AISP 04 - ÁREA SUDOESTE DE GOIÂNIA', 'as': 4},
    {'location': 'AISP 05 - ÁREA OESTE DE GOIÂNIA', 'as': 5},
    {'location': 'AISP 06 - ÁREA SUL DE GOIÂNIA', 'as': 6},
    {'location': 'AISP 07 - ÁREA LESTE DE GOIÂNIA', 'as': 7}]


to_save = []
repository = SSPRepository()
for year in years:
    for nature in natures:
        for location in locations:
            result = repository.get_day_week_by_city(year, nature['nature'], location['location'])
            for idx, current in enumerate(result['resultset']):
                to_save.append(
                    ['{}-01-0{}'.format(year, idx + 1),
                     current[1] if current[1] else 0])

np_array = numpy.asarray(to_save)
df = pd.DataFrame(np_array)
df.to_csv("roubos_goiania_regiao.csv", index=False)


locations = [
    {'location': 'GOIÂNIA', 'as': 'GOIÂNIA'}]

to_save = []
repository = SSPRepository()
for year in years:
    for nature in natures:
        for location in locations:
            result = repository.get_months_by_city(year, nature['nature'], location['location'])
            for current in result['resultset']:
                to_save.append(
                    ['{}-{}-01'.format(current[1], FULL_MONTHS[current[0]]),
                     current[2] if current[2] else 0])

np_array = numpy.asarray(to_save)
df = pd.DataFrame(np_array)
df.to_csv("roubos_goiania.csv", index=False)
