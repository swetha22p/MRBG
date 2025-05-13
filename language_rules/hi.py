morpho_seman = {
    'superl': ('before', 'sabase'),
    'comparmore': ('before', 'aXika'),
    'comparless': ('before', 'kama'),
}

TAM_DICT_FILES = {
    'hi': './repository/tam_mapping_hin.dat'

}
# Language-specific verb rules for Hindi
VERB_RULES = {
    'default_tam': 'pres',
    'special_verbs': {
        'hE': {
            'pres': {'root': 'hE', 'tam': 'pres'},
            'past': {'root': 'WA', 'tam': 'past'}
        },
        'jA': {
            'yA': {'root': 'jA', 'tam': 'yA1'}
        }
    },
    'causative': {
        'default_causative_verb': 'karwA',
        'double_causative_verb': 'lawA',
        'mapping': {
            'karnA': 'karwA',
            'dEnA': 'dilwA'
        }
    }
}
spkview_list_b = [
    'jI', 'lagAwAra', 'kevala' ,'karIba','TIka','mAwra','basa','sirPa',
]
spkview_list_a = [
    'hI', 'BI', 'jI', 'wo','sI','ki','waka', 'lagaBaga', 'lagAwAra'
]
#hi.py
SPKVIEW_TO_WORD_MAP={}
