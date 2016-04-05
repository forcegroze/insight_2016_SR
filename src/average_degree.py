#########Insight coding challenge 2016 - Twitter average degree over 60s window#########

import time
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir_input = os.path.join(current_dir, '../tweet_input/tweets.txt')
target_dir_output = os.path.join(current_dir, '../tweet_output/output.txt')

index_regulator = []
average_degree_regulator = 0

##############Extracting timing and hashtags from each entry###################
def extract_timing_hashtags(filename):
    timing = list()
    hashtags = list()
    counter = 0
    bad_input_counter = 0
    with open(filename, 'rb') as input:
        for line in input:

            ###Checking if the line starts with the correct formatting - date, time extraction into list###
            if str.startswith(line,'''{"created_at":'''):
                creation_data = line.strip().split('''{"created_at":''')
                date = creation_data[1].strip().split('''"''')[1]
                date_formatted = date.split(' ')
                date_formatted = date_formatted[1]+' '+date_formatted[2]+' '+date_formatted[3]+' '+date_formatted[5]
                timing.append(date_formatted)
                counter += 1


                ###Once correct date/time formatting is present, hashtag formatting is checked###
                hashtag_data = line.strip().split('''{"hashtags":''')
                if hashtag_data[1][0:2] == "[]":
                    hashtags.append([])

                ###Individual Hashtags are extracted into list###
                elif hashtag_data[1][0:2] != "[]":
                    hashtag = hashtag_data[1].split('''{"text":''')
                    i = 0
                    hashtags_temp = []
                    for hashes in hashtag:
                        hashes = hashes.replace('"','')
                        hashes = hashes.split(",")[0]
                        if i > 0:
                            hashtags_temp.append(hashes)
                        i += 1
                    hashtags.append(hashtags_temp)

            else:
                bad_input_counter += 0

        ###Running 60s window###
        if len(timing) >= 2:
            initiate_time_windows(timing, hashtags)

        #print(timing)
        #print(hashtags)
        #print("There are %s bad inputs out of %s inputs.") % (bad_input_counter, counter)




###############Initiating 60s window####################
def initiate_time_windows(timing, hashtags):

    unique_elements_window = []
    connecting_elements = {}

    ###Time/Date formatting is established###
    for index, time_formatted in enumerate(timing):
        struct_time = time.strptime(time_formatted, "%b %d %H:%M:%S %Y")

        ###Moving time window is initiated###
        for index2, time_formatted2 in enumerate(timing):
            if index2 > index:
                struct_time2 = time.strptime(time_formatted2, "%b %d %H:%M:%S %Y")
                time_window_seconds = abs(time.mktime(struct_time2) - time.mktime(struct_time))

                ###If the time difference is within 60s, average degree is calculated###
                if time_window_seconds <= 60:

                    average_degree_calculation(hashtags, index, unique_elements_window, connecting_elements)

    ###Calculating average degree from last line###
    index = index2
    last_line_calculator(hashtags, index, unique_elements_window, connecting_elements)

#################Extracting nodes, edges and average degree in 60s window##################
def average_degree_calculation(hashtags, index, unique_elements_window, connecting_elements):

    global index_regulator
    global average_degree_regulator
    ###Calculating hashtag edge list and nodes###
    if hashtags[index] != []:
        if len(hashtags[index]) > 1:
            for primary_hash_index, primary_hash in enumerate(hashtags[index]):

                ###Calculating unique hashtags###
                if primary_hash not in unique_elements_window:
                    unique_elements_window.append(primary_hash)

                for secondary_hash_index, secondary_hash in enumerate(hashtags[index]):
                    ####Remove repeating hashtags and progress comparisons###
                    if primary_hash != secondary_hash and secondary_hash_index > primary_hash_index:
                        if connecting_elements.has_key(primary_hash) and secondary_hash not in connecting_elements[primary_hash]:
                            connecting_elements[primary_hash].append(secondary_hash)
                        else:
                            connecting_elements[primary_hash] = [secondary_hash]

                        if connecting_elements.has_key(secondary_hash) and primary_hash not in connecting_elements[secondary_hash]:
                            connecting_elements[secondary_hash].append(primary_hash)
                        else:
                            connecting_elements[secondary_hash] = [primary_hash]


        else:
            unique_elements_window.append(hashtags[index][0])


        ###Calculating number of edges(connecting elements), nodes(unique elements) and average degree###
        total_unique_elements = len(unique_elements_window)
        total_connecting_elements = sum(len(edges) for edges in connecting_elements.values())
        average_degree = float(total_connecting_elements)/float(total_unique_elements)
        average_degree_regulator = average_degree

    else:
        average_degree_print = '%.2f' % (average_degree_regulator)
        average_degree_out.writelines(average_degree_print + "\n")

        ###Index regulator for printing average degree###
    if index not in index_regulator and hashtags[index] != []:
        #print(index)
        average_degree_print = '%.2f' % (average_degree_regulator)
        average_degree_out.writelines(average_degree_print + "\n")
        index_regulator.append(index)

###Calculating last line of tweets###
def last_line_calculator(hashtags, index, unique_elements_window, connecting_elements):
    global average_degree_regulator

    if hashtags[index] != []:
        average_degree_calculation(hashtags, index, unique_elements_window, connecting_elements)
    else:
        average_degree_print = '%.2f' % (average_degree_regulator)
        average_degree_out.writelines(average_degree_print + "\n")


###Write average degree output to text file###
average_degree_out = open(target_dir_output, 'w')
extract_timing_hashtags(target_dir_input)
average_degree_out.close()



















