import requests


class SSPRepository:
    def __init__(self):
        self.session_request = requests.session()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': 'JSESSIONID={}'.format(self.auth())}
        self.url = 'http://pentaho.ssp.go.gov.br/pentaho/content/cda/doQuery?'

    def get_months(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': 'Filter({Generate([LocalidadeFato.RispAisp].Children, [LocalidadeFato.RispAisp].CurrentMember.Children)}, ([Measures].[AispNome] = "' + location + '"))',
            'parampar_mes_fechado': 'Dezembro',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_months_by_city(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': '[LocalidadeFato.EstadoCidadeBairro].[GO].[' + location + ']',
            'parampar_mes_fechado': 'Dezembro',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_day_week_by_city(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': '[LocalidadeFato.EstadoCidadeBairro].[GO].[' + location + ']',
            'parampar_mes_fechado': 'Dezembro',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART_SEMANA',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_day_week(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': 'Filter({Generate([LocalidadeFato.RispAisp].Children, [LocalidadeFato.RispAisp].CurrentMember.Children)}, ([Measures].[AispNome] = "' + location + '"))',
            'parampar_mes_fechado': 'Março',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART_SEMANA',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_day_week(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': 'Filter({Generate([LocalidadeFato.RispAisp].Children, [LocalidadeFato.RispAisp].CurrentMember.Children)}, ([Measures].[AispNome] = "' + location + '"))',
            'parampar_mes_fechado': 'Março',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART_SEMANA',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_hour(self, year: int, nature: str, location: str):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': location,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': 'Filter({Generate([LocalidadeFato.RispAisp].Children, [LocalidadeFato.RispAisp].CurrentMember.Children)}, ([Measures].[AispNome] = "' + location + '"))',
            'parampar_mes_fechado': 'Março',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART_HORA',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_neighborhood(self, location: str):
        payload = {
            'parampar_localidade': location,
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'QUERY_SELEC_BAIRRO',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def get_months_by_neighborhood(self, year: int, nature: str, location: str, city: str = 'GOIÂNIA'):
        payload = {
            'parampar_natureza_mdx': nature,
            'parampar_ano': str(year),
            'parampar_mes': '',
            'parampar_localidade': city,
            'parampar_ano_final': '',
            'parampar_mes_final': '',
            'parampar_ano_anterior': str(year - 1),
            'parampar_localidade_mdx': '[LocalidadeFato.EstadoCidadeBairro].[GO].[' + city + '].[' + location + ']',
            'parampar_mes_fechado': 'Dezembro',
            'path': '/observatorio/paineis/mapaPublico/painel_publico.cda',
            'dataAccessId': 'DS_MDX_OCORRENCIAS_CHART',
            'outputIndexId': '1',
            'pageSize': '0',
            'pageStart': '0',
            'sortBy': '',
            'paramsearchBox': ''}
        return self.session_request.post(self.url, headers=self.headers, data=payload).json()

    def auth(self):
        auth = 'http://pentaho.ssp.go.gov.br/pentaho/content/pentaho-cdf-dd/Render?solution=observatorio&path=%2Fpaineis%2FmapaPublico&file=painel_publico.wcdf&userid=anonymousUser&password=anonymousUser'
        self.session_request.get(auth)
        return self.session_request.cookies.get_dict()['JSESSIONID']
