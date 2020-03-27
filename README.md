# music2graph
## Purpose
In this work is proposed a method to trasform a music sheet in mxl or MIDI file format in a multi-feature-graph witch represent the composition's music style.
## Tecnologies
To extract the elements Notes, Chord, Rest and music metadata from music files, is used the Python MIT Toolkist [music21](https://web.mit.edu/music21/) and to generate the associated graph is used the Python library [NetworkX](https://networkx.github.io/).
## Music Informations
- Note contains information about a note into the file, some are: pitch, duration, beat, interval between 2 notes, octave
- Rest contains all information about a rest into the file, some are: duration and beat
- Chord contains all information about a chord into the files, some are: name, duration, beat.

## Graph Structure
The Python library NetworkX is used to create a graph, which maps the music composition and, in particular, every graph represents a music instrument part (voice).
The graph contains information into nodes, that are wrapped in two different structures: (a)Key, (b)Node.

For every voice into music file is created a graph, the KeyNode has double function; one contains all musical composition metadata such as Metromark, Time Signature and others, and second is the marker for a voice, because for every voice into the musical composition there is a graph, while the second structure is a wrapper for the classes Note, Rest or Chord.
Every Node is linked with an edge to the relative KeyNode and KeyNodes are linked each others.

## Music style representation
Often in classical music there are more than a voice and in many case, notes on different voices are played together or their durations incorporate other notes.
This is the only case when Notes of different voices are linked each others.
