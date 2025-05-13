import sys
from repository.common_v4 import *

def process_input(input_text, lang="eng", concept_file="dictionaries/concept-to-mrs-rels.dat"):
    """
    Processes the input text, replacing words based on a concept dictionary.
    
    Parameters:
    input_text (str): The input text containing tagged sentences.
    lang (str): The language to process ('eng', 'hin', 'skt'). Defaults to 'eng'.
    concept_file (str): Path to the concept-to-mrs-rels.dat dictionary.

    Returns:
    str: The processed text with words replaced based on the dictionary.
    """
    
    if lang == "hin":
        column_to_check = 1
    elif lang == "skt":
        column_to_check = 2
    else:
        column_to_check = 1  # Default to Hindi if unspecified

    # Load the concept dictionary
    concept_dict = {}
    try:
        with open(concept_file, "r", encoding="utf-8") as f:
            for row in f:
                cols = row.strip().split()
                if len(cols) >= 4:
                    key = cols[2] if lang == "skt" else cols[1]
                    concept_dict[key] = cols[3]
    except FileNotFoundError:
        print(f"Error: Concept file '{concept_file}' not found.")
        return input_text  # Return original text if dictionary file is missing

    lines = input_text.split("\n")
    updated_lines = []

    for line in lines:
        words = line.split()

        # Skip metadata and comments
        if not words or words[0].startswith(("<", "#", "%")):
            updated_lines.append(line)
            continue

        # Replace word if found in concept_dict
        if words[0] in concept_dict:
            words[0] = concept_dict[words[0]]
        elif '-' in words[0]:  # Handle hyphenated words
            base_word, suffix = words[0].split('-', 1)
            words[0] = concept_dict.get(base_word, base_word) + '-' + suffix
        if words[4] == '0:main':
            main_verb_tam = words[0]
            base_word = main_verb_tam.split("-")[0]
            tam_term = identify_tam_terms(main_verb_tam)
            words[0] = base_word+'-'+tam_term
       

        updated_lines.append(" ".join(words))

    return "\n".join(updated_lines)

