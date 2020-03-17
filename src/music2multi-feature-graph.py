from music21 import *
from src import Note, Chord, Rest, KeyNode, Node
import networkx as nx


'''
All nodes are linked with the KeyNode and every nodes is linked to previously node and following node.
:param G: The input graph
:param idGraph: input graph's number id 
:param key_node: KeyNode's id of the graph G
:param node_count: node's number id
:param keyElement: KeyNode of the graph G
'''
def link_voice_notes(G, idGraph, key_node, node_count, keyElement):
    if node_count == 1:
        nodeKey = Node("", "")
        nodeKey.id = idGraph
        nodeKey.music_element = keyElement
        G.add_node(key_node, element=nodeKey)
        G.add_edge(key_node, node_count)
    else:
        prec_node = node_count - 1
        G.add_edge(prec_node, node_count)
        G.add_edge(key_node, node_count)
    node_count = node_count + 1
    return node_count


'''
top function provides to link all wrapped notes witch duration matching with the other notes played from the other voice.
the matching criteria is explained in READme.

:param voices_graph: list of graphs
'''
def top(voices_graphs):
    i = 0
    j = 1
    index_start_graph = []
    index_start_graph.append(0)
    cache_len = 0
    for i in range(len(voices_graphs) - 1):
        cache_len += len(voices_graphs[i])
        index_start_graph.append(cache_len)
    i = 0
    union_graph = nx.disjoint_union_all(voices_graphs)
    while i < len(voices_graphs):
        while j < len(voices_graphs):
            if i == j:
                return
            discard = 0
            first_graph = voices_graphs[i]
            second_graph = voices_graphs[j]
            longest_graph = ''
            if len(first_graph) >= len(second_graph):
                longest_graph = first_graph
            else:
                longest_graph = second_graph
            voice_increase = ''
            discard_voice = ''
            k = 0
            el_voice1 = 1
            el_voice2 = 1
            count_v1 = index_start_graph[i]
            count_v2 = index_start_graph[j]
            union_graph.add_edge(count_v1, count_v2)
            count_v1 = count_v1 + 1
            count_v2 = count_v2 + 1
            while k < len(longest_graph) and el_voice1 < len(first_graph) and el_voice2 < len(second_graph):
                v1 = first_graph.nodes[el_voice1]['element']
                v2 = second_graph.nodes[el_voice2]['element']
                skip_script = False
                if v1.music_element.measure == v2.music_element.measure:
                    union_graph.add_edge(count_v1, count_v2)
                    if discard > 0:
                        if v1.music_element.duration >= v2.music_element.duration:
                            if discard_voice == 'voice1':
                                discard = discard - v2.music_element.duration
                                voice_increase = 'voice2'
                                if discard == 0:
                                    skip_script = True
                            elif discard_voice == 'voice2':
                                discard = v1.music_element.duration - discard
                                voice_increase = 'voice2'
                                discard_voice = 'voice1'
                        else:
                            if discard_voice == 'voice2':
                                discard = discard - v1.music_element.duration
                                voice_increase = 'voice1'
                                if discard == 0:
                                    skip_script = True
                            elif discard_voice == 'voice1':
                                discard = v2.music_element.duration - discard
                                voice_increase = 'voice1'
                                discard_voice = 'voice2'
                    if discard == 0 and skip_script is False:
                        if v1.music_element.duration >= v2.music_element.duration:
                            discard = v1.music_element.duration - v2.music_element.duration
                            voice_increase = 'voice2'
                            discard_voice = 'voice1'
                        else:
                            discard = v2.music_element.duration - v1.music_element.duration
                            voice_increase = 'voice1'
                            discard_voice = 'voice2'
                    if discard == 0:
                        el_voice1 = el_voice1 + 1
                        count_v1 = count_v1 + 1
                        el_voice2 = el_voice2 + 1
                        count_v2 = count_v2 + 1
                    elif discard > 0:
                        if voice_increase == 'voice2':
                            el_voice2 = el_voice2 + 1
                            count_v2 = count_v2 + 1
                        elif voice_increase == 'voice1':
                            el_voice1 = el_voice1 + 1
                            count_v1 = count_v1 + 1
                k = k + 1
            j = j + 1
        i = i + 1
        j = i + 1


'''
Function to trasform a musical composition file (suggest MIDI or mxl files) in an undirected graph.
The graph has a first node (KeyNode) containing the composition metadata, the other Nodes contains music data.
All nodes are linked with the KeyNode and every nodes is linked to previously node and following node.

:param musical_composition_file: musical composition file
'''
def get_notes_chords_rests(musical_composition_file):
    if isinstance(musical_composition_file, str):
        score = converter.parse(musical_composition_file)
    else:
        score = musical_composition_file
    # prec_note is used to calculate the interval between two following notes
    prec_note = ''
    c = 0
    # a list of graphs
    voices_graphs = []
    idGraph = -1
    for entry in score.recurse():
        if isinstance(entry, stream.Part):
            # graph associated to the music part
            G = nx.Graph()
            # the first node in the graph with voice info EX: time, clef, instrument
            idGraph = idGraph + 1
            key_node = 0
            keyNodeV = KeyNode("", "", "", "", "")
            # count for nodes, first node is for the key node voice
            node_count = 1
            #measure count
            measure_count = 0
        if isinstance(entry, stream.Measure):
            measure_count = measure_count + 1
        if isinstance(entry, instrument.Instrument):
            keyNodeV.instrument = str(entry)
        if isinstance(entry, tempo.MetronomeMark):
            keyNodeV.metro = str(entry)
        if isinstance(entry, key.Key):
            keyNodeV.key = str(entry)
        if isinstance(entry, meter.TimeSignature):
            keyNodeV.time_signature = str(entry)
        if isinstance(entry, clef.Clef):
            keyNodeV.clef = str(entry)
        if isinstance(entry, note.Note):
            # counter for identify the first note and set the interval
            if c is 0:
                prec_note = entry.pitch
                c = c + 1
            # intervalCalculator is the value of the interval
            intervalCalculator = interval.Interval(noteStart=prec_note, noteEnd=entry)
            my_note = Note(entry.pitch.name, entry.pitch.octave, entry.duration.quarterLength, entry.beat, intervalCalculator.simpleName, measure_count)
            elementNode = Node(idGraph, my_note)
            G.add_node(node_count, element=elementNode)
            node_count = link_voice_notes(G, idGraph, key_node, node_count, keyNodeV)
            prec_note = entry.pitch
        elif isinstance(entry, chord.Chord):
            my_chord = Chord(entry.pitchNames, entry.duration.quarterLength, entry.beat, measure_count)
            elementNode = Node(idGraph, my_chord)
            G.add_node(node_count, element=elementNode)
            node_count = link_voice_notes(G, idGraph, key_node, node_count, keyNodeV)
        elif isinstance(entry, note.Rest):
            my_rest = Rest('Rest', 0, entry.duration.quarterLength, entry.beat, measure_count)
            elementNode = Node(idGraph, my_rest)
            G.add_node(node_count, element=elementNode)
            node_count = link_voice_notes(G, idGraph, key_node, node_count, keyNodeV)
        # condition to understand if the voice is finished
        elif isinstance(entry, bar.Barline) and entry.type == 'final':
            voices_graphs.append(G)
    return voices_graphs





