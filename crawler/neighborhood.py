from datetime import datetime

from SSPRepository import SSPRepository
from database import Database
from models import NeighborhoodQuantity

db = Database()
repository = SSPRepository()
FULL_MONTHS = {'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
               'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
               'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'}

# ## Save neighborhood on database
#
# neighborhood = repository.get_neighborhood('GOIÂNIA')
# print(neighborhood)
# db = Database()
# with db.db_session() as session:
#     try:
#         for current in neighborhood['resultset']:
#
#             if current[0] != 0:
#                 save = Neighborhood(id=current[0], name=current[1])
#                 session.add(save)
#
#         session.commit()
#     except Exception as e:
#         print(e)
#         session.rollback()


# Save quantity theft neighborhood on database

neighborhood = repository.get_neighborhood('GOIÂNIA')

# Captura os dados de 2 em 2 anos
years = [2012, 2014, 2016]

# Selecionando a natureza de crime
nature = '[Natureza].[CRIMES CONTRA O PATRIMÔNIO].[CPB ART. 157 CAPUT: ROUBO].[ROUBO A TRANSEUNTE]'

with db.db_session() as session:
    for year in years:
        repository = SSPRepository()
        for location in neighborhood['resultset']:
            if location[0] != 0:
                try:
                    result = repository.get_months_by_neighborhood(year, nature, location[1])
                    print(result['resultset'])
                    for current in result['resultset']:
                        save = NeighborhoodQuantity(neighborhood_id=location[0], date_occurrence=datetime.strptime(
                            '{}-{}-01'.format(current[1], FULL_MONTHS[current[0]]), "%Y-%m-%d"),
                                                    theft=current[2] if current[2] else 0)
                        session.add(save)
                    session.commit()
                except Exception as e:
                    session.commit()
                    print('{}-{}'.format(year, location[1]))
                    print(e)
