morpho_seman = {
    'superl': ('before', 'most'),
    'comparmore': ('before', 'more'),
    'comparless': ('before', 'less'),
}


TAM_DICT_FILES = {
    'en': './repository/tam_mapping_eng.dat'
    # Add more languages as needed
}
# Language-specific verb rules for English
VERB_RULES = {
    'default_tam': 'base',
    'special_verbs': {},
    'causative': {
        'default_causative_verb': 'make',
        'double_causative_verb': 'ask',
        'mapping': {}
    }
}

# Define the lookup table as a dictionary
PPPOST_MAP = {
    'k7t': 'at',
    'k3': 'with',
    'k5': 'from',
    'k5prk': 'from',
    'k7': 'on',
    'k7p': 'in',
    'k7a': 'according to',
    'k4': 'to',
    'k2': 'to',
    'k2p': 'to',
    'rblak': 'after',
    'rt': 'for',
    'rblpk': 'before',
    'rn': 'among',
    'rd': 'towards',
    'rp': 'through',
    'rask1': 'along with',
    'rask2': 'along with',
    'rask3': 'along with',
    'rask4': 'along with',
    'rask5': 'along with',
    'k1as': 'along with',
    'k2as': 'along with',
    'k3as': 'along with',
    'k4as': 'along with',
    'k5as': 'along with',
    'k7as': 'along with',
    'r6': 'of',
    'quantless': 'less than',
    'quantmore': 'more than',
    'rkl': 'after',
    'rh': 'because of',
    'rasneg': 'without',
    'rv': 'than',
}


# rules/en.py
spkview_list_b = [
    'jI', 'lagAwAra', 'kevala' ,'karIba','TIka','mAwra','basa','sirPa',
]
spkview_list_a = [
    'hI', 'BI', 'jI', 'wo','sI','ki','waka', 'lagaBaga', 'lagAwAra','def'
]

SPKVIEW_TO_WORD_MAP = {
    'hI_6': 'Only',
    'BI_1': 'also',
    'BI_3': 'any',
    'BI_4': 'Yet',
    'BI_5': 'Still',
    'kevala_1': 'only',
    'kariba_1': 'Nearly',
    'lagaBAga_1': 'Almost',
    'sirPa_1': 'Only',
    'def': 'the',  
}