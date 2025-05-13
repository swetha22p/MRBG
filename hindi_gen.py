import sys
import json
from repository.common_v4 import *
from repository.USR_to_JSON import USR_to_json
from repository.coref_discourse import *
from repository.constant import *
from map_concept import process_input
from repository.construction import *
from repository.reorder import rearrange_tuples,arrange_by_index_order
from repository.morph_gen import en_generate_morph,hi_generate_morph
from repository.preprocessing import process_segment,preprocess_id
from repository.identify_cat import identify_cat
from repository.process_cat import process_all_cat,process_change
from repository.Check_words_in_dict import check_words_in_dict,identify_words_in_corpus, transform_data_star
import argparse
# from my_masking_mask import *


# Main function that handles the core processing logic
def process_file_data(input_data,segment_id,lang):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, HAS_MORPHO_SEMANTIC_DATA, HAS_DISCOURSE_DATA, HAS_COREF
    global flag_conj, flag_disjunct, flag_span, flag_cp, flag_meas, flag_rate, flag_spatial, flag_waw, flag_cal, flag_xvanxva, flag_temporal_spatial, k1_not_need, has_changes, global_starred_words

    # Initialize flags and output data list
    try:
        reset_global_dicts()
        rules_info = generate_rulesinfo(input_data) #Extracting Rules from each row of USR
        
        # Extracting Information
        src_sentence = rules_info[0]
        root_words = rules_info[1]
        index_data = [int(x) for x in rules_info[2]]
        seman_data = rules_info[3]
        gnp_data = rules_info[4]
        depend_data = rules_info[5]
        discourse_data = rules_info[6]
        spkview_data = rules_info[7]
        scope_data = rules_info[8]
        construction_data = rules_info[9]
        sentence_type = rules_info[10]

        if sentence_type[1:] in pass_list:
            k1_not_need=True
        
        # check_main_verb(depend_data)
        # try:
            # if sentence_type[1:] not in 
        check_main_verb(depend_data)
        #     if not has_main_verb:
        #         raise Exception("Main verb is missing in the dependency data")
        # except Exception as e:
        #     print('ERROR_1:',e)
        #     PP_fulldata_dict_with_id = create_dict_with_ids(segment_id, str(e).splitlines()[-1])
        #     return PP_fulldata_dict_with_id


        # Making a collection of words and its rules as a list of tuples.
        words_info = generate_wordinfo(root_words, index_data, seman_data,
                                    gnp_data, depend_data, discourse_data, spkview_data,scope_data,construction_data)
        categorized_words_list= identify_cat(words_info,sentence_type,lang)
        depend_data, HAS_CONSTRUCTION_DATA, flags = identify_and_assign_dep(root_words, construction_data, depend_data, index_data, spkview_data)

        if spkview_data != [] or len(spkview_data) > 0:
            HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data,discourse_data,index_data,lang)
        if any(discourse_data):
            HAS_DISCOURSE_DATA = True
        if any('coref' in item for item in discourse_data):
            HAS_COREF = True
        for info in words_info:
            if info[4] == '0:main':
                main_verb_tam = info[1]
        tam_term =main_verb_tam.split("-")[1]
        
        # print(words_info,'wf')
        # index_order,words_info = rearrange_tuples(words_info)
        # foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data 
     

        #  Processing Stage - identify the cat and proces each cat
        processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words= process_all_cat(
            categorized_words_list,index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes,lang)
        
        # processed_words = arrange_by_index_order(processed_words, index_order)
        
        if HAS_CONSTRUCTION_DATA:
            processed_words, flags = process_construction(processed_words, root_words, construction_data, depend_data, 
                                gnp_data, index_data, flags)
        language_config = {
            'en': {
                'func': en_generate_morph,
                'args': ['processed_words', 'tam_term', 'depend_data', 'sentence_type']
            },
            'hi': {
                'func': hi_generate_morph,
                'args': ['processed_words']
            }
        }

        # Build a kwargs dict dynamically from local variables (or passed-in context)
        context = {
            'processed_words': processed_words,
            'tam_term': tam_term,
            'depend_data': depend_data,
            'sentence_type': sentence_type,
            'lang': lang
        }
        handler = language_config[lang]['func']
        arg_names = language_config[lang]['args']

        # Pick only needed args from context
        call_args = [context[arg] for arg in arg_names]

        # Input for morph generator is generated and fed into it.
        # Generator outputs the result in a file named morph_input.txt-out.txt
        outputData = handler(*call_args)
        # Check for any non-generated words (mainly noun) & change the gender for non-generated words
    
        # # -> is for the concept which is in dict but its morph data is not found
        # * -> then the conept is not found in dict
        # has_changes, processed_nouns = handle_unprocessed(index_order,depend_data,outputData, processed_nouns, construction_data)
        # has_star, processed_words = handle_star(index_data,outputData,processed_words)
        has_changes, processed_nouns = handle_unprocessed(index_data,depend_data,outputData, processed_nouns, construction_data)
        # handle unprocessed_verbs also with verb agreement
        # If any changes is done in gender for any word.
        # Adjectives and verbs are re-processed as they might be dependent on it.
        if has_changes:
            # Reprocessing adjectives and verbs based on new noun info
            processed_words = process_change(
                rules_info,
                categorized_words_list,
                words_info,
                processed_nouns,
                processed_pronouns,
                processed_others,
                processed_foreign_words,
                processed_indeclinables,
                lang
            )
            
            # Sentence is generated again if HAS_CONSTRUCTION_DATA is True
            if HAS_CONSTRUCTION_DATA:
                processed_words, flags = process_construction(
                    processed_words,
                    root_words,
                    construction_data,
                    depend_data,
                    gnp_data,
                    index_data,
                    flags
                )

            # Generate morphological output if has_changes is True
            outputData = handler(*call_args)
            

        outputData, global_starred_words, has_star = check_words_in_dict(outputData,processed_words,global_starred_words)
        processed_words_after_star = analyse_output_data(outputData, processed_words)
        if has_star:
            # Only generate morphological output if has_star is True
            if lang == "hi":
                outputData, response_data, replaced_indices = identify_words_in_corpus(global_starred_words,outputData,lang)
                processed_words_after_star = analyse_output_data(outputData, processed_words)
                outputData = handler(*call_args)
                outputData = transform_data_star(response_data, replaced_indices, outputData)

        # outputData = check_words_in_dict(outputData,processed_words)
        # Post-Processing Stage
        # generated words and word-info data is combined #pp data not yet added
        # outputData = replace_word(outputData,response_data)
        transformed_data = analyse_output_data(outputData, processed_words)

        log(f'postpositions: {processed_postpositions_dict}')
        PP_fulldata = add_postposition(transformed_data,index_data,depend_data, processed_postpositions_dict)
        
        #construction data is joined
        if HAS_CONSTRUCTION_DATA:
            log(f'construct: {construction_dict}')
            PP_fulldata = add_construction(PP_fulldata, construction_dict)
        
        if HAS_SPKVIEW_DATA:
            log(f'spkview: {spkview_dict}')
            PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

        HAS_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(index_data,gnp_data, PP_fulldata,words_info,lang)
        if HAS_MORPHO_SEMANTIC_DATA:
            log(f'MORPHO SEMANTIC: {MORPHO_SEMANTIC_DICT}')
            PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

        # if HAS_ADDITIONAL_WORDS:
        #     PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)
        # print(PP_fulldata,'lkl')
        # print(PP_fulldata_dict_with_id,'kkk')
        PP_fulldata_dict_with_id = create_dict_with_ids(segment_id, PP_fulldata)
        log(f'PP_fulldata_dict_with_id: {PP_fulldata_dict_with_id}')
        return PP_fulldata_dict_with_id
    
    except Exception as e:
            # Return the last line of the error message
        log(f'ERROR_2:{e}', 'ERROR')
        error = create_dict_with_ids(segment_id, str(e))
        # return str(e).splitlines()[-1]
        return error
    
def hindi_generation(input_text,lang):
    """
    Process Hindi text input, extracting sentences, segment IDs, and generating structured output.
    """
    PP_fulldata_dict_with_ids = {}
    input_text = preprocess_id(input_text)
    segments = parse_segments(input_text)

    sentences, all_output, segment_ids = [], [], []
    parser = USR_to_json(input_text)
    parser.parse_input_text()
    construction_json = generate_construction_json(parser.parse_input_text())
    coref_json,coref_dict,sentence_type_dict = process_coreferences(parser.parse_input_text())
    disource_json=transform_data(parser.parse_input_text())

    with open('construction.json', 'w', encoding='utf-8') as f:
        json.dump(construction_json, f, ensure_ascii=False, indent=2)
    with open("discource.json", "w") as file:
        json.dump(disource_json, file, indent=4)
    with open("output.json", "w") as file:
        json.dump(parser.parse_input_text(), file, indent=4)

    for segment in segments:
        segment_id, sentence, output = process_segment(segment)
        if segment_id:
            segment_ids.append(segment_id)
        if output:
            try:
                output1=process_file_data(output,segment_id,lang)
                PP_fulldata_dict_with_ids.update(output1)
            except Exception as e:
                print(f'[ERROR_3]:{e}')
                all_output.append(f"Error processing {segment_id}: {str(e).splitlines()[-1]}")
    
    PP_fulldata_dict_with_ids = update_morph_dict_coref(coref_json, PP_fulldata_dict_with_ids)
    
    filtered_data = filter_and_concat_data(PP_fulldata_dict_with_ids,sentence_type_dict)
    
    with open('generated_data.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    filtered_data = update_discourse_sentences(disource_json, filtered_data)
    print("filtered_data",filtered_data)
    
    masked_hindi_data=collect_hindi_output(filtered_data)
    # below comented fun are for mask 
    # json_output1 = convert_sentences_to_json(all_output)
    # all_output=process_masked_multiple_sentences(json_output1)
    last_output = process_sentence(masked_hindi_data, sentences)
    log(global_starred_words, 'Global starred words with categories')
    log(f'hindi_generation output : {last_output}')
    return last_output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process linguistic input and generate output.')
    parser.add_argument('--lang', type=str, default='en', help='Language code (e.g., "en" or "hi")')
    
    args = parser.parse_args()
    lang = args.lang
    input_data='''
<sent_id=gold_data_032>
#राम मोहन से कम बुद्धिमान है।
rAma 1 per/male - 4:k1 - - - -
mohana 2 per/male - 1:rv - - - -
buxXimAna_1 3 - comparless 4:k1s - - - -
hE_1-pres 4 - - 0:main - - - -
%affirmative
</sent_id>
'''
    # file_path = './ncert_11stnd_bk1_usr4correction_output.txt'
    #     <sent_id=gold_data_084>
# #राम मोहन से कम बदमाश है।
# rAma 1 per/male - 5:k1 - - - -
# mohana 2 per/male - 1:rv - - - -
# baxamASa_1 4 - comparless 4:k1s - - - -
# hE_1-pres 5 - - 0:main - - - -
# %affirmative
# </sent_id>
    
    
    # # Read input data from the file
    # input_data = read_file(file_path)
    
    if lang == 'en':
       input_data  = process_input(input_data)
    hindi_generation(input_data,lang)
# [{"segment_id": "7a", "text": "ना केवल वे आज्ञाकारी ही थे।"}, {"segment_id": "7b", "text": "बल्कि वे बहुत समझदार भी थे भी।"}]}
