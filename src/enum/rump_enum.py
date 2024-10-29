from enum import Enum


class ClassificationRumpEnum(Enum):
    AUSENTE = {'model_id':'1', 'database_id':'1'}
    ESCASSA = {'model_id':'2', 'database_id':'3'}
    MEDIANA = {'model_id':'3', 'database_id':'6'}
    UNIFORME = {'model_id':'4', 'database_id':'8'}
    EXCESSIVA = {'model_id':'5', 'database_id':'9'}

    POSITIVE = {'database_id': 'positive'}
    NEGATIVE = {'database_id': 'negative'}
    IN_COMPLIANCE = {'database_id': 'in_compliance'}
    BRUISE = {'database_id': 'bruise'}
    FAILURE = {'database_id': 'failure'}
    FAILURE_BRUISE = {'database_id': 'failure/bruise'}
    UNCLASSIFIED = {'database_id': 'unclassified'}