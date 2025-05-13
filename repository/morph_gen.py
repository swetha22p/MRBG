import subprocess
from repository.constant import *
from repository.common_v4 import log

def hi_generate_morph(processed_words):
    """Run Morph generator"""
    morph_input = generate_input_for_morph_generator(processed_words)
    MORPH_INPUT = write_data(morph_input)
    OUTPUT_FILE1 = run_morph_generator(MORPH_INPUT)
    log(f"Output of Morph Generator : {OUTPUT_FILE1}")
    return OUTPUT_FILE1

def en_generate_morph(processed_words, tam_term, depend_data, sentence_type):
    morph_input = generate_input_for_en_morph_generator(processed_words, tam_term, depend_data, sentence_type)
    final_morph_input = format_morph_input(morph_input)
    # mappings = parse_file("best_matches_output_uniq.txt")
    # morph_input1,replaced_words = update_list_with_index(morph_input, mappings)
    MORPH_INPUT = write_data(final_morph_input)
    OUTPUT_FILE1 = run_en_morph_generator(MORPH_INPUT)
    # print(OUTPUT_FILE1,'ooooooooo')
    # OUTPUT_FILE = replace_words_in_sentence_with_index(OUTPUT_FILE1, replaced_words)
    # OUTPUT_FILE = check_words_in_dict(OUTPUT_FILE)
    #print(OUTPUT_FILE,'output')
    return OUTPUT_FILE1

def generate_input_for_morph_generator(input_data):
    """Process the input and generate the input for morph generator"""
    morph_input_data = []
    for data in input_data:
        # if data[1] in construction_list:
        #     continue
        if data[2] == 'p':
            if data[8] != None and isinstance(data[8], str):
                morph_data = f'^{data[1]}<cat:{data[2]}><parsarg:{data[7]}><fnum:{data[8]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
            else:
                morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><parsarg:{data[7]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
        elif data[2] == 'n' and data[7] in ('proper', 'digit'):
            morph_data = f'{data[1]}'
        # elif data[2] == 'n' and data[7] == 'vn':
        #     morph_data = f'^{data[1]}<cat:{data[7]}><case:{data[3]}>$'
        elif data[2] == 'vn':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}>$'
        elif data[2] == 'n' and data[7] != 'proper':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'
        elif data[2] == 'v' and data[8] in ('main','auxiliary'):
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] == 'kara' and data[8] in ('nonfinite','adverb')     :
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] != 'kara' and data[8] =='nonfinite':
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><case:{data[7]}><tam:{data[6]}>$'
        elif data[2] == 'adj':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'
        elif data[2] == 'vj':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'indec':
            morph_data = f'{data[1]}'
        elif data[2] == 'other':
            morph_data = f'{data[1]}'
        else:
            morph_data = f'^{data[1]}$'
        morph_input_data.append(morph_data)
    #print(morph_input_data)
    print(morph_input_data)
    return morph_input_data


word=''
def generate_input_for_en_morph_generator(input_data, tam_term, depend_data, sentence_type):
    global word
    """Load auxiliary data and process the input for the morph generator."""
    input_data = [
        tuple('be' if item == 'statecopula' else item for item in tup)
        for tup in input_data if 'ne' not in tup
    ]
    morph_input_final_tup = []
    depend_dict = {
        i + 1: (item.split(':')[1] if ':' in item and len(item.split(':')) > 1 else '')
        for i, item in enumerate(depend_data)
    }

    moph_tuples = []
    
    # Load auxiliary data from TSV file
    # with open("repository/tam_morph_tuple.tsv", 'r', encoding='utf-8') as file:
    #     reader = csv.reader(file, delimiter='\t')
    #     next(reader)  # Skip header row  
    #     for row in reader:
    #         if len(row) < 6:
    #             continue  # Skip incomplete rows
    #         english_tam = row[3].strip()
    #         tuple_info = row[5].strip()
    #         if tam_term == english_tam:
    #             moph_tuples = tuple(eval(part) for part in tuple_info.split(';'))
                
    for i, data in enumerate(input_data):
        morph_input_tuple = None  # Reset for each iteration
        person_mapping = {'a': 'p3', 'm_1': 'p2', 'u': 'p1'}
        data = list(data)  # Convert tuple to list so we can modify it
        
        if len(data)>6:
            if isinstance(data[6], list):
                A = data[6]
                new_list = []

                # Flatten the weird string list into proper tokens
                cleaned_tokens = []
                for token in A:
                    # Remove parentheses and quotes and split
                    token = token.replace('(', '').replace(')', '').replace("'", "").strip()
                    cleaned_tokens.extend([t.strip() for t in token.split(',')])
                
                for item in cleaned_tokens:
                    if item == 'per':
                        new_list.append(person_mapping.get(data[5], data[5]))
                    elif item == 'num':
                        if data[4] == "s":
                            data[4] = "sg"
                        else:
                            data[4] = 'pl'
                        new_list.append(data[4])
                    else:
                        new_list.append(item)
                
                data[6] = new_list  # Update the list inside the tuple
                
                # If you intended to use new_list for further processing, assign it to morph_input_tuple
                # If you only needed to update data[6], you might not even need this line.
                # For now, we'll assign the new_list tuple to morph_input_tuple.
                morph_input_tuple = tuple(new_list)
            
        # Continue with the rest of your conditions
            if data[2] != 'adj' and data[2] == 'v':
                person = person_mapping.get(data[5], None)
                number = 'sg' if data[4] == 's' else 'pl'
                gender = data[3]
            if data[2] == 'n' or data[2] == 'p':
                person = person_mapping.get(data[6], None)
                number = 'sg' if data[5] == 's' else 'pl'
                gender = data[4]
                word = data[1]

            if data[2] == 'p' and data[1] == 'this':
                morph_input_tuple = (data[1], 'det', 'dem', number)  
            elif data[2] == 'p' and data[1] == 'that':
                morph_input_tuple = (data[1], 'prn', 'dem', 'mf', number)
            elif data[2] == 'p' and data[0] in depend_dict and depend_dict[data[0]] in ['k2', 'k4']:
                morph_input_tuple = ('prpers', 'prn', 'obj', person, gender, number)
            elif data[2] == 'p':
                morph_input_tuple = ('prpers','prn', 'subj', person, gender, number) 
            elif data[2] == 'n' and data[1] in ['not', 'after', 'before', 'near', 'far']:
                morph_input_tuple = (data[1], 'adv')
            elif data[2] == 'n' and data[7] == 'proper':  
                morph_input_tuple = (data[1], 'np', 'ant', gender, number)   
            elif data[2] == 'n' and data[7] != 'proper':
                morph_input_tuple = (data[1], data[2], number)
            elif data[2] == 'v':
                if 'es' in data or 'pres' in data:
                    morph_input_tuple = (data[1],'vblex','pres', person, number)
                elif 'ed' in data:
                    morph_input_tuple = (data[1],'vblex','past')
                elif 'ing' in data:
                    morph_input_tuple = (data[1],'vblex','pprs')
                elif data[6] == "0":
                    morph_input_tuple = (data[1],'vblex','imp')
                else:
                    morph_input_tuple = (data[1],'vblex','inf')
           
            elif (sentence_type[1:] in ['negative', 'interrogative'] and tam_term == 'wA_hE_1'):
                morph_input_tuple = ('do', 'vaux', 'pres')
        if data[2] == 'adj':
            morph_input_tuple = (data[1],'adj','sint')
            
        if morph_input_tuple: 
            morph_input_final_tup.append(morph_input_tuple)

    # Further post-processing steps remain the same
    morph_input_final_tup = [
        tuple(word if item == 'vm' else item for item in tup)
        for tup in morph_input_final_tup
    ]
    morph_input_final_tup = [
        tuple(person if item == 'per' else item for item in tup)
        for tup in morph_input_final_tup
    ]
    morph_input_final_tup = [
        tuple(number if item == 'num' else item for item in tup)
        for tup in morph_input_final_tup
    ]

    morph_input_final_tuple = []
    for tup in morph_input_final_tup:
        word = tup[0]
        index = next((data[0] for data in input_data if data[1] == word), None)
        
        if index is not None:
            morph_input_final_tuple.append((index,) + tup)
        else:
            morph_input_final_tuple.append((-1,) + tup)  # Use -1 if no match found

    return morph_input_final_tuple


def format_morph_input(morph_input_final_tuple):
    """Formats the morph input data into the required structure."""
    morph_input_format = []
    
    for item in morph_input_final_tuple:
        if isinstance(item, tuple) and item:
            word = item[1]
            
            # Check if the last element is a special marker (e.g., "# to")
            if item[-1].startswith('#'):
                tags = ''.join(f'<{tag}>' for tag in item[2:-1])  # Exclude last element
                marker = item[-1]  # Store the marker separately
            else:
                tags = ''.join(f'<{tag}>' for tag in item[2:])
                marker = ''
            
            # Construct the formatted string
            formatted_str = f'^{word}{tags}{marker}$'
            morph_input_format.append(formatted_str)
    
    return morph_input_format


def write_data(writedata):
    """Return the Morph Input Data as a string instead of writing to a file."""
    final_input = " ".join(writedata)
    # Return the generated morph data as a string
    # ##print(final_input,'final')
    return final_input

import subprocess

def run_morph_generator(data):
    """Pass the morph generator through the provided data and return the output for Hindi."""
    command = [
        "lt-proc",
        "-g",
        "-c",
        "repository/hi.gen_LC.bin",
    ]

    # Run the command with input data piped directly
    result = subprocess.run(
        command,
        input=data,
        capture_output=True,
        text=True
    )

    # Optionally, handle errors
    if result.returncode != 0:
        raise RuntimeError(f"Error in Hindi morph generator: {result.stderr}")

    return result.stdout

def run_en_morph_generator(data):
    """Pass the morph generator through the provided data and return the output for English."""
    command = [
        "lt-proc",
        "-g",
        "-c",
        "apertium_eng/eng.autogen.bin",
    ]

    # Run the command with input data piped directly
    result = subprocess.run(
        command,
        input=data,
        capture_output=True,
        text=True
    )

    # Optionally, handle errors
    if result.returncode != 0:
        raise RuntimeError(f"Error in English morph generator: {result.stderr}")

    return result.stdout
