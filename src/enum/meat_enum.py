from enum import Enum


class MeatEnum(Enum):
    AUSENTE = {'model_id':'1', 'database_id':'1'}
    ESCASSA = {'model_id':'2', 'database_id':'3'}
    MEDIANA = {'model_id':'3', 'database_id':'6'}
    MEDIANA_UNIFORME = {'model_id':'3', 'database_id':'6'}
    UNIFORME = {'model_id':'4', 'database_id':'8'}
    EXCESSIVA = {'model_id':'5', 'database_id':'9'}

    GRADO_0 = {'model_id': '1', 'database_id': '1'}
    GRADO_1 = {'model_id': '2', 'database_id': '3'}
    GRADO_2 = {'model_id': '3', 'database_id': '6'}
    GRADO_3 = {'model_id': '4', 'database_id': '8'}

