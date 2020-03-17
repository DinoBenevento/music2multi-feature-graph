from src import KeyNode
import networkx as nx
import os
import pickle
import itertools


'''
Function to walk int graphs presented in voices_graph and in union_graph joined.
:param voice_graphs: list of graphs 
:param union_graph: graph join of graphs in voice_graph
:param dicts: list of dictionaries
:param index_start_graph: list of the first node's index of every single graph in union_graph and in union_graph joined.
:param name_comp: composition_name
'''
def walk_graphs(voices_graphs, union_graph, dicts, index_start_graph, name_comp):
    cache_graph = ''
    iteration_time = 0
    count_file_save = 0
    while iteration_time < len(union_graph):
        cache_graph, count_file_save = create_combinations(voices_graphs, iteration_time, dicts, cache_graph, union_graph, index_start_graph, count_file_save, name_comp)
        iteration_time = iteration_time + 1
        index = 0
        while index < len(voices_graphs):
            if index_start_graph[index] < len(union_graph) - 1:
                index_start_graph[index] = index_start_graph[index] + 1
                index = index + 1
            else:
                print('Next notes combination saved')
                return



def create_combinations(graphs, iteration_time, dicts, cache_graph, union_graph, index_start_graph, count_file_save, name_comp):
    gt = nx.Graph()
    if iteration_time == 0:
        reduced_combination = []
        combinations_position = set_combination_positions(index_start_graph)
        for c in range(len(combinations_position)):
            if c < len(index_start_graph):
                for comb in combinations_position[c]:
                    reduced_combination.append(comb)
            else:
                break
        i = 0
        while i < len(graphs):
            gi = graphs[i]
            key_node_gi = gi.nodes[0]['element']
            gt.add_node(index_start_graph[i], element=key_node_gi)
            i = i + 1
        save_combinations(reduced_combination, union_graph, iteration_time, 0, dicts,name_comp)
        return gt, count_file_save
    elif iteration_time > 0:
        count_combination = 0
        gt = cache_graph.copy()
        complete_gt = cache_graph.copy()
        reduced_combination = []
        combinations_position = set_combination_positions(index_start_graph)
        for c in range(len(combinations_position)):
            if c < len(index_start_graph):
                for comb in combinations_position[c]:
                    reduced_combination.append(comb)
            else:
                break
        cache_reduced_list = []
        for z in range(len(combinations_position)):
            index_combination = []
            for comb in combinations_position[z]:
                index_combination.append(comb)
            for i in index_combination:
                gt.add_node(i, element=union_graph.nodes[i]['element'])
                reduced_combination.remove(i)
                cache_reduced_list.append(i)
            count_combination += 1
            gt = cache_graph.copy()
            for i in cache_reduced_list:
                reduced_combination.append(i)
            cache_reduced_list.clear()
        for i in index_start_graph:
            complete_gt.add_node(i, element=union_graph.nodes[i]['element'])
        return complete_gt, count_file_save


def set_combination_positions(index_start_graph):
    combination_positions = []
    for i in range(1, len(index_start_graph)):
        l1 = itertools.combinations(index_start_graph, i)
        for e in l1:
            combination_positions.append(e)
    return combination_positions


def save_combinations(reduced_combination, union_graph, iter, count_combination, dicts, n_comp):
    count_file = 0
    for comb in reduced_combination:
            proc_voice = []
            proc_note_pitch = []
            proc_note_duration = []
            proc_note_octave = []
            index_voice = []
            index_voice.append(comb)
            for i in index_voice:
                if i + 1 < len(union_graph):
                    if not isinstance(union_graph.nodes[i + 1]['element'].music_element, KeyNode):
                        proc_voice.append(union_graph.nodes[i + 1]['element'].id)
                        proc_note_pitch.append(union_graph.nodes[i + 1]['element'].music_element.name)
                        proc_note_octave.append(union_graph.nodes[i + 1]['element'].music_element.octave)
                        proc_note_duration.append(union_graph.nodes[i + 1]['element'].music_element.duration)
                    else:
                        proc_voice.append(-1)
                        proc_note_pitch.append("Mute")
                        proc_note_octave.append(0)
                        proc_note_duration.append(0.0)
                elif i + 1 >= len(union_graph):
                    proc_voice.append(-1)
                    proc_note_pitch.append("Mute")
                    proc_note_octave.append(0)
                    proc_note_duration.append(0.0)
            path = 'C:/Users/io/Desktop/Proc_Voices_Dataset/' + str(n_comp)+'/'
            if not os.path.exists(path):
                os.mkdir(path)
            iterString = str(iter) + str(count_combination) + str(count_file)
            count_file += 1
            if iter < 10:
                sub_dir = path + str(0) + str(iter)
            else:
                sub_dir = path + str(iter)
            if not os.path.exists(sub_dir):
                os.mkdir(sub_dir)
            path_file = sub_dir + '/' + iterString
            my_data_voice = []
            my_data_pitch_octave_duration = []
            dict_note = dicts[0]
            for j in range(len(proc_voice)):
                my_data_voice.append(float(proc_voice[j]))
                my_data_pitch_octave_duration.append([float(dict_note[proc_note_pitch[j]]), proc_note_octave[j], proc_note_duration[j]])
            pickle.dump(my_data_voice, open(path_file + 'v.pickle', 'wb'))
            pickle.dump(my_data_pitch_octave_duration, open(path_file + 'pd.pickle', 'wb'))