from generated_conditions import get_ppost

def preprocess_postposition_new(concept_type, np_data, words_info, verb_data, index_data):
    '''Calculates postposition to words wherever applicable according to rules.'''
    cp_verb_list = ['prayApreprsa+kara', 'sahAyawA+kara']
    
    # Initialize variables to default values.
    data_case = ''
    data_index = None
    data_head = None
    ppost = ''
    new_case = 'o'

    if len(verb_data) > 0:
        verb_term = verb_data[1]
        if len(verb_term) > 0:
            root_main = verb_term.strip().split('-')[0].split('_')[0]

    # Check that np_data is not empty and has the expected elements.
    if np_data != () and len(np_data) > 4 and np_data[4] != '':
        try:
            parts = np_data[4].strip().split(':')
            if len(parts) >= 2:
                data_head = parts[0]
                data_case = parts[1]
            else:
                data_case = ''
        except Exception as e:
            print(f"Error processing np_data[4]: {e}")
            data_case = ''

        data_index = np_data[0]
        data_seman = np_data[2]

        # Call generated function with all possible context
        ppost = get_ppost(
            data_case,
            data_seman=data_seman,
            root_main=root_main if 'root_main' in locals() else None,
            concept_type=concept_type
        )

    return new_case, ppost