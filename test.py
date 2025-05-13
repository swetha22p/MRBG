# import json
# import openpyxl

# # Function to process the sentences and save results to an Excel file
# def extract_names_to_excel(file_path, output_file_path):
#     # Initialize a list to store the results
#     result = []

#     # Read the file content
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = file.read()

#     # Split the data into individual sentences (assuming each sentence starts with <Sentence id=)
#     sentences = data.split("<Sentence id=")

#     # Process each sentence
#     for sentence in sentences:
#         if not sentence.strip():
#             continue  # Skip empty entries

#         # Extract the sentence ID
#         sentence_id = sentence.split('>')[0].strip("'")

#         # Initialize lists for r6-k1 and r6-k2 names
#         r6_k1_lists = []  # List of lists for r6-k1 dependencies
#         r6_k2_lists = []  # List of lists for r6-k2 dependencies

#         # Parse the sentence further to check for r6-k1 or r6-k2
#         lines = sentence.split('\n')
#         inside_r6_k1 = False
#         inside_r6_k2 = False
#         current_r6_k1_list = []
#         current_r6_k2_list = []

#         for line in lines:
#             # Check if we are entering an r6-k1 block
#             if "drel='r6-k1" in line:
#                 if inside_r6_k1 and current_r6_k1_list:
#                     r6_k1_lists.append(current_r6_k1_list)  # Save the previous r6-k1 list
#                 inside_r6_k1 = True
#                 inside_r6_k2 = False
#                 current_r6_k1_list = []  # Start a new r6-k1 list
#                 continue

#             # Check if we are entering an r6-k2 block
#             if "drel='r6-k2" in line:
#                 if inside_r6_k2 and current_r6_k2_list:
#                     r6_k2_lists.append(current_r6_k2_list)  # Save the previous r6-k2 list
#                 inside_r6_k2 = True
#                 inside_r6_k1 = False
#                 current_r6_k2_list = []  # Start a new r6-k2 list
#                 continue

#             # Extract names for r6-k1
#             if inside_r6_k1 and "name='" in line:
#                 name_start = line.find("name='") + len("name='")
#                 name_end = line.find("'", name_start)
#                 name = line[name_start:name_end]
#                 current_r6_k1_list.append(name)

#             # Extract names for r6-k2
#             if inside_r6_k2 and "name='" in line:
#                 name_start = line.find("name='") + len("name='")
#                 name_end = line.find("'", name_start)
#                 name = line[name_start:name_end]
#                 current_r6_k2_list.append(name)

#             # Exit the block if we encounter the closing parenthesis
#             if "))" in line:
#                 if inside_r6_k1 and current_r6_k1_list:
#                     r6_k1_lists.append(current_r6_k1_list)  # Save the last r6-k1 list
#                     inside_r6_k1 = False
#                 if inside_r6_k2 and current_r6_k2_list:
#                     r6_k2_lists.append(current_r6_k2_list)  # Save the last r6-k2 list
#                     inside_r6_k2 = False

#         # If names were found, store them along with the sentence ID
#         if r6_k1_lists or r6_k2_lists:
#             result.append({
#                 "sentence_id": sentence_id,
#                 "r6_k1_lists": r6_k1_lists,
#                 "r6_k2_lists": r6_k2_lists
#             })

#     # Write the results to an Excel file
#     workbook = openpyxl.Workbook()
#     sheet = workbook.active
#     sheet.title = "Extracted Data"

#     # Add headers
#     sheet.append(["Sentence ID", "r6_k1", "r6_k2"])

#     # Add data rows
#     for entry in result:
#         sentence_id = entry["sentence_id"]
#         r6_k1_lists = entry["r6_k1_lists"]
#         r6_k2_lists = entry["r6_k2_lists"]

#         # Handle r6_k1_lists
#         if r6_k1_lists:
#             for sublist in r6_k1_lists:
#                 r6_k1_string = " + ".join(sublist)
#                 sheet.append([sentence_id, r6_k1_string, ""])
        
#         # Handle r6_k2_lists
#         if r6_k2_lists:
#             for sublist in r6_k2_lists:
#                 r6_k2_string = " + ".join(sublist)
#                 sheet.append([sentence_id, "", r6_k2_string])

#         # If both r6_k1_lists and r6_k2_lists are empty, add an empty row
#         if not r6_k1_lists and not r6_k2_lists:
#             sheet.append([sentence_id, "", ""])

#     # Save the workbook
#     workbook.save(output_file_path)
#     print(f"Results have been written to {output_file_path}")

# # Example usage
# file_path = "/mnt/e/UBUNTU/Hindi_usr_generation/hindi_generator_mask/project_usr/data/ALL"  # Replace with the path to your file
#   # Replace with the path to your input file  # Replace with the path to your input file
# output_file_path = "output_results.xlsx"  # Replace with the desired output file path
# extract_names_to_excel(file_path, output_file_path)

def transform_data(response_data, replaced_indices, output_sentence):
    """
    Transforms the given response_data and replaced_indices into a structured dictionary,
    and modifies the output sentence based on the processed data.

    Args:
        response_data (dict): A dictionary with one or more key-value pairs.
        replaced_indices (dict): A dictionary mapping indices to replacement words.
        output_sentence (str): The original sentence to transform.

    Returns:
        str: The transformed sentence.
    """
    try:
        # Step 1: Validate inputs
        if not isinstance(response_data, dict) or not isinstance(replaced_indices, dict):
            raise ValueError("Both response_data and replaced_indices must be dictionaries.")
        
        if not output_sentence.strip():
            raise ValueError("output_sentence cannot be empty.")

        # Ensure response_data and replaced_indices have the same number of entries
        if len(response_data) != len(replaced_indices):
            raise ValueError("response_data and replaced_indices must have the same number of entries.")

        # Step 2: Process each star_word and its corresponding index-word pair
        for (star_word, paradigm), (index_in_sentence, new_word) in zip(response_data.items(), replaced_indices.items()):
            # Ensure paradigm has the expected structure
            if not isinstance(paradigm, list) or len(paradigm) < 1:
                raise ValueError(f"Paradigm for '{star_word}' is invalid.")
            
            paradigm_pattern = paradigm[0]  # Extract the pattern string from the paradigm

            # Call transform_sentence for the current star_word and index-word pair
            transformed_sentence = transform_sentence(
                output=output_sentence,  # Corrected parameter name
                transformed_data={
                    "star_word": star_word,
                    "paradigm": paradigm,
                    "index_in_sentence": index_in_sentence,
                    "new_word": new_word
                }
            )
            
            # Update the output_sentence with the transformed result
            output_sentence = transformed_sentence

        return output_sentence

    except Exception as e:
        return f"Error in transform_data: {str(e)}"


def transform_sentence(output, transformed_data):
    """
    Transforms a sentence by modifying the star_word based on the paradigm and replacing
    the word at the specified index in the output sentence.

    Args:
        output (str): The original sentence to transform.
        transformed_data (dict): The dictionary containing transformation details.

    Returns:
        str: The transformed sentence.
    """
    try:
        # Extract components from transformed_data
        star_word = transformed_data["star_word"]
        paradigm = transformed_data["paradigm"]
        index_in_sentence = transformed_data["index_in_sentence"]
        new_word = transformed_data["new_word"]

        # Step 1: Process the paradigm
        paradigm_pattern = paradigm[0]  # Extract the pattern string from the paradigm
        
        # Ensure the paradigm contains a '/'
        if '/' not in paradigm_pattern:
            raise ValueError("Paradigm pattern must contain a '/'")
        
        before_slash, after_slash = paradigm_pattern.split('/')
        
        # Ensure the after_slash contains '__'
        if '__' not in after_slash:
            raise ValueError("After-slash part of paradigm must contain '__'")
        
        char_to_remove = after_slash.split('__')[0]  # Get the character to remove

        # Step 2: Modify the star_word
        # Remove char_to_remove ONLY if it appears at the end of the star_word
        if star_word.endswith(char_to_remove):
            modified_star_word = star_word[:-len(char_to_remove)]  # Remove the last len(char_to_remove) characters
        else:
            modified_star_word = star_word  # No change if char_to_remove is not at the end

        # Step 3: Process the target word at index_in_sentence
        words = output.split()  # Split the output into a list of words

        # Ensure index_in_sentence is within bounds
        if index_in_sentence >= len(words):
            raise IndexError("Index out of range in the output sentence")

        target_word = words[index_in_sentence]  # Extract the word at the specified index

        # Split the target word into parts based on '/'
        parts = target_word.replace('#','').split('/')

        # Transform each part
        transformed_parts = []
        for part in parts:
            # Remove the prefix (before_slash) from the part
            remaining_suffix = part.replace(before_slash, '')
            # Construct the transformed part
            transformed_part = f"{modified_star_word}{remaining_suffix}"
            transformed_parts.append(transformed_part)

        # Join the transformed parts back together with '/'
        transformed_word = '/'.join(transformed_parts)

        # Replace the word at index_in_sentence with the transformed word
        words[index_in_sentence] = transformed_word
        transformed_output = ' '.join(words)  # Join the words back into a sentence

        return transformed_output

    except Exception as e:
        return f"Error in transform_sentence: {str(e)}"
if __name__ == "__main__":
    # Example Input
    response_data = {
        'Anwarika': ['wIn/a__adj', 0, 2],
        'saMkenxrIya': ['wIn/a__adj', 1, 1],
        'mEMtala': ['calaciwr/a__n', 1, 1],
        'sWalamaMdala': ['Karc/a__n', 1, 2]
        
    }
    replaced_indices = {
        1: 'wIna',
        5: 'wIna',
        9: 'calaciwra',
        10: 'Karca'
    }
    output_sentence = 'pqWvI #wIna BAga 3 ##pramuKa #wIna ##parawa hE kroda calaciwra Karca'

    # Transform the sentence
    result = transform_data(response_data, replaced_indices, output_sentence)
    print(result)
# star_word = "mAnaciwrakAra"
# paradigm = ["Karc/__n", 1, 2]
# index_in_sentence = 3
# new_word = "Karca"
# output = 'varwamAna #isa prakAra Karca/KarcoM #badI mAzga hE'

# 'saMkenxrIya': ['wIn/a__adj', 1, 1]} {1: 'wIna', 5: 'wIna', 9: 'calaciwra', 10: 'Karca'}

# # Call the function and print the result
# result = transform_sentence(star_word, paradigm, index_in_sentence, new_word, output)
# print(result)