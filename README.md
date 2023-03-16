## jbt-simulator
<img src="img/icon.png" width="128px">

It is a simulator that plays musical scores in the format on mac/windows.

## Demo
<img src="screenshots/sample01.png" width="512px">

## Example

### Prepare sheet music and music
Please prepare the musical score in the [fumen format #memo2](http://yosh52.web.fc2.com/jubeat/fumenformat.html) 
and the MP3 file corresponding to it.


Your site [cosmos memo](https://www53.atwiki.jp/cosmos_memo/) for sheet music data will be helpful．

### Environment
- python 3.10.5
- pygame 2.3.0
- gevent 22.10.2
- mutagen 1.46.0
- numpy 1.24.2

#### Notice
If you are building an environment using pyenv or anaconda under the mac environment,
pygame can't get keyboard events.

### Execution

When running `main.py`, pass the paths in this order: `music file` and `score file`.

The music file format is `utf-8` text file.

Hold sheet music is currently not supported.

```shell
python main.py music/hogehoge.mp3 fumen/fugafuga.jbt
```

### Function

#### Song seek

The horizontal axis of the screen is linked to the playback position of the music.

The playback time of the song is set to 100%, 
* tapping the left end of the screen seeks to the 0% position, 
* tapping the center seeks to the 50% position, 
* tapping the right end seeks to the 100% position.

At the same time as moving the playback position of the music, 
the playback position of the marker is also automatically corrected.

## [WIP] Function 👷
Basically, it conforms to jubeatLab.
- Music playback
  - Arbitrary speed, seek
- Music notation

## [WIP] Algorithm for playing music from jubeat-memo format
```
2

口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```

- From **|** to **|** is called **1 beat**

- 1 beat is **4 beats** and **1 bar** <-- important here
  - Since one measure is 4 beats, the number of measures (2, 16, etc.) before the measure is irrelevant for parsing.
  - It's just added to make it easier to see when editing.
  - In the example below, using the conditions that make up this bar, when the position information cannot be defined in four lines, it is divided and expressed.
    - Since the position of ⑭ overlaps with ③, the 16th measure is divided into two measures. **However, the generated bar data is for ① bar.** 

```
16
口⑧口① |①②③④|
⑥⑨②⑩ |⑤⑥⑦⑧|
⑫③⑪④ |⑨⑩⑪⑫|
⑬⑤口⑦ |⑬ー⑭ー|

口口口口
口口口口
口⑭口口
口口口口
```

 
## Forms that compose a musical score
### Note type
- The smallest unit that composes a musical score
- Note(note: String, t: Double, position: Int, bpm: Double)
- note; Key (①, ②, ...) to identify the note in that measure
- bpm; BPM at which the note appears
- t; the time the note should be tapped in the current bar

```
2
t=60
口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```

  - Example of ① notes in the second bar above
```
Since the bpm is 60, there are 60 beats per minute.

That is, 1000ms per beat, 250ms per note,

In other words, ① Notes is determined as Note(①, 250, 4, 60).
```
- position; Panel number (1-16) that the note should display
```
Panel number correspondence table;

01  02  03  04
05  06  07  08
09  10  11  12
13  14  15  16
```

### Measure type
- collection of Note types
- Measure(measure: Int, notes: List < Note >)
- measure; how many bars
- notes; measure Array of Note type that appears in the bar

### Chart type
- collection of Measure
- Compose the entire score
- Chart(difficulty: Difficulty, level: Int, measures: List < Measure >)
- difficulty; Degree of difficulty (BASIC or ADVANCED or EXTREME)
- level; lv1 to lv10
- measures; Array of bars

### Music type
- Hold song information
- One-to-one correspondence with music data
- Music(title: String, artist: String, charts: List < Chart >)
- title; song name
- artist; artist name
- charts; Musical score data corresponding to one song data (basically there are 3 difficulty levels)

```
>> music.print()
Music(hogehoge, fugafuga, 
Chart(Difficulty.BASIC, 3, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
Chart(Difficulty.ADVANCED, 7, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
Chart(Difficulty.EXTREME, 9, 
Measure(1, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(2, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
Measure(3, 
Note(①, 250.0000, 01, 160.0000)
Note(②, 500.0000, 02, 160.0000)
Note(③, 750.0000, 03, 160.0000)
)
)
--------------------------------
)
```

## Analysis algorithm
- For now, read the score file line by line
- Consider reading the data in the second bar of the example below.
- By the way, there are two timings when Notes data is generated.
```
2
t=60
口口口① |①ーーー|

口④口口 |ーーーー|

口口③口 |ーー②ー|

口②口口 |③ー④ー|
```
- In step ④ above, **notes data is generated from board data**. 
  When ④ first appears, the information that the display position is the 6th panel can be grasped, 
  but the display time is in an undetermined state. 
  That is, Note(④, None, 6, 60). None means undetermined.

- In ② above, **notes data is generated from time data**. When ② first appears, 
  the information that the display time is **11x250=2750ms** can be grasped, but the display position is in an undetermined state. 
  That is, Note(②, 2750, None 60). None means undetermined.

## Analyze [fumen/sample.jbt](fumen/sample.jbt)
In jbt-simulator, each bar is expressed as a measure (placement data, timing data),

Each music sheet is managed by an array of measures called measures.

For example, if the score data of the second measure in the output result of `sample.jbt` is read, 
it will be as follows.
```
2 ['口口口①口④口口口口③口口②口口', ['①ーーー', 'ーーーー', 'ーー②ー', '③ー④ー']]
```

Below is the result of reading and analyzing `fumen/sample.jbt`.
len(measures) becomes 81, match the number of bars in `sample.jbt`.
When one measure is expressed across multiple measures like the 15th measure, 
the placement data is automatically linked.

```
1 ['口口口口口口口口口口口口口口口口', ['ーーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
2 ['口口口①口④口口口口③口口②口口', ['①ーーー', 'ーーーー', 'ーー②ー', '③ー④ー']]
3 ['口⑥①口③口口⑤口口口口④口②口', ['①ー②ー', '③ー④ー', '⑤ーーー', '⑥ーーー']]
4 ['⑧口口⑨⑦⑥④口口⑤③②口口口①', ['①②③④', '⑤⑥⑦⑧', '⑨ーーー', 'ーーーー']]
5 ['⑧④②⑥口口口口口口口口③⑦⑤①', ['①②ーー', '③④ーー', '⑤⑥ーー', '⑦⑧ーー']]
6 ['⑦口口口口①⑥口口口③口⑧⑤④②', ['①ー②ー', 'ー③④ー', 'ーー⑤⑥', '⑦ー⑧ー']]
7 ['口口③①口⑤口口⑦口口口⑧⑥④②', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
8 ['口口口口口口⑥①口口③口⑦⑤④②', ['①ー②ー', 'ー③④ー', 'ーー⑤⑥', 'ーー⑦ー']]
9 ['口口口口口⑥口口口口②口⑤④③①', ['ーー①ー', 'ー②③ー', 'ーー④ー', 'ーー⑤⑥']]
10 ['⑤⑤①④③⑧①口②③⑥①口⑦口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ー⑧ー']]
11 ['口②①口口⑥⑤口⑥⑤④③②④③①', ['①ーーー', '②ーーー', '③ー④ー', '⑤ー⑥ー']]
12 ['④口①⑤①⑥⑤口口⑧⑦③①口③②', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ー⑧ー']]
13 ['④②①③④④③③口口口口②④③①', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
14 ['⑥⑦⑧口口⑪⑩⑨④口③②口口⑤①', ['①ー②ー', '③④⑤ー', '⑥ー⑦ー⑧ー', '⑨ー⑩ー⑪ー']]
15 ['⑥⑥⑧口口⑧口⑧②③⑧④①⑤⑦⑦口口口口口口口口⑨口口口⑩口口口', ['①ー②ー', '③④⑤ー', '⑥ー⑦ー', '⑧ー⑨⑩']]
16 ['口⑧口①⑥⑨②⑩⑫③⑪④⑬⑤口⑦口口口口口口口口口⑭口口口口口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
17 ['③③①①⑦⑦⑤⑤⑧⑨⑨口⑩④②⑥', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ーーー']]
18 ['①口口＜口口口口口口口口口①＜口②口④口口口③⑤口口②⑥口②口⑦', ['①ーーー', 'ーーーー', '②ー③ー④ー', '⑤ー⑥ー⑦ー']]
19 ['⑨①⑨①④⑤⑥口③⑨⑦口②口⑧口口⑪口⑩口口口口口口口口口⑬口⑫', ['①②③④', '⑤⑥⑦⑧', '⑨ーーー', '⑩⑪⑫⑬']]
20 ['④⑥⑤⑤③口⑧⑤②口⑦口①口⑤口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
21 ['③⑨⑧④③⑤⑧④①口⑥②①⑦口②', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー']]
22 ['②⑪⑩②③⑫⑨口④⑬⑧①⑤⑥⑦①', ['①ーーー', '②③④⑤', '⑥⑦⑧⑨', '⑩⑪⑫⑬']]
23 ['⑤⑨⑧④口⑩口③口⑪口②⑥⑫⑦①', ['①②③④', '⑤ー⑥ー', '⑦ー⑧ー', '⑨⑩⑪⑫']]
24 ['⑤⑭⑭④⑥⑫⑨③⑦⑪⑩②⑧口⑬①', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
25 ['②口⑥⑥④口⑥①③口口①口⑤⑤①⑦⑦口口口⑦口口口口口口口口口口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', 'ーー⑦ー']]
26 ['口⑨⑨口④口⑥口①⑤③⑦①⑧⑧②⑩口口口口口口⑪⑩口口口口口口⑪', ['①ー②③', '④⑤⑥⑦', '⑧ー⑨ー', '⑩ー⑪ー']]
27 ['⑨⑦⑥①①②⑤口口③④⑧⑨口口口口口口⑩口口口口⑪口口口口口⑪口', ['①ー②③', '④⑤⑥⑦', '⑧ー⑨ー', '⑩⑪ーー']]
28 ['⑦⑤⑨口口①口口口②⑥⑧⑦③⑨④', ['①②③ー', '④ー⑤ー', '⑥ー⑦ー', '⑧ー⑨ー']]
29 ['⑨④口②⑤④③②口⑥③口⑦①口⑧', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー']]
30 ['口⑧⑦①⑫⑨⑥⑬②⑩⑤③口⑪④口', ['①②③ー', '④⑤⑥⑦', '⑧⑨⑩⑪', '⑫ー⑬ー']]
31 ['⑤⑧⑤⑨口口⑦口口⑥④③⑥口①②', ['①②③④', '⑤ー⑥ー', 'ーー⑦⑧', '⑨ーーー']]
32 ['⑬口⑬口⑤⑥⑦⑧⑫⑪⑩⑨④③②①口口口口口口口口口口口口口⑭口⑭', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬ー⑭ー']]
33 ['⑥⑦口①⑤③⑥口口④口口②口①口口口⑧⑧口口口口口口口口口口口口', ['①ー②ー', '③ー④ー', '⑤ー⑥⑦', 'ーー⑧ー']]
34 ['口⑤口口④⑥口①⑤口①口②③③①口口口口口口⑦口口口⑧口口口口⑦', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧ー']]
35 ['①⑤⑤①口口口口②口⑦③⑥②口④', ['ーー①ー', '②③ーー', '④ー⑤⑥', '⑦ーーー']]
36 ['②⑦⑧①②②①①③④⑤⑥口②①口口口口⑨口口口口口口口口⑩口口口', ['①ーーー', '②ーーー', '③④⑤⑥⑦⑧', '⑨ー⑩ー']]
37 ['⑤口口⑧①⑥⑨③⑦口口⑩口②④口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー⑩ー']]
38 ['口⑤口口④⑥口①⑤口①口②③③①口口口口口口⑦口口口⑧口口口口⑦', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧ー']]
39 ['①⑤⑤①口口口口②口⑦③⑥②口④', ['ーー①ー', '②③ーー', '④ー⑤⑥', '⑦ーーー']]
40 ['口⑦⑧⑨①①②②③④⑤⑥⑩①②口', ['①ーーー', '②ーーー', '③④⑤⑥⑦⑧', '⑨ー⑩ー']]
41 ['⑤口口⑧①⑥⑨③⑦口口⑩口②④口', ['①ー②ー', '③ー④ー', '⑤ー⑥ー⑦ー', '⑧ー⑨ー⑩ー']]
42 ['口③④④⑥⑥口⑤⑦口②口口①口口', ['①ー②ー', '③ーーー', '④ー⑤ー', '⑥ー⑦ー']]
43 ['②口②口口口①口口①④①③口①口', ['ーーーー', '①ーーー', '②ー③ー', '④ーーー']]
44 ['②③口①②②①①口⑥⑤④口②①口', ['①ーーー', '②ーーー', '③ーーー', '④⑤⑥ー']]
45 ['①⑦⑥⑦②口⑨口③口口口④⑧⑧⑤', ['①②③④⑤ーーー', '⑥ーーー', '⑦ーー⑧', 'ーー⑨ー']]
46 ['①④口④①①口③②口③③口⑤口口口口口口⑥口⑥口口口口口口口⑦口', ['①ーーー', '②ー③ー', '④ー⑤ー', '⑥ー⑦ー']]
47 ['⑧⑤①口⑦④⑩口⑥③⑨口②口口口口口⑪口口口口口口口口口口口口口', ['①ー②ー', '③ー④ー⑤ー', '⑥ー⑦ー⑧ー', '⑨ー⑩ー⑪ー']]
48 ['⑤④⑥⑤④③⑦⑥③②⑧⑦②①①⑧', ['①ー②ー', '③ー④ー', '⑤ー⑥ー', '⑦ー⑧ー']]
49 ['口④④口③②口④②③⑤口⑤①①⑤口口口口口⑥⑥口口口口口口⑥⑥口', ['①ー②ー', '③ーーー', '④ーー⑤', 'ーー⑥ー']]
50 ['①口＜口口口口口①口＜口口口口口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
51 ['①口口口口＞口①①口口口口＞口①', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
52 ['口①口＜口口口①口①口＜口口口①', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
53 ['口①口口＞口①口口①口口＞口①口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
54 ['①②③④口口①口＞①口口口口①口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
55 ['口口口口口口口①口①①＜口口口口口口口口口口口口口口口②口口④③', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
56 ['口口口口＞①口口③口①口②①口口口口口口④口口口口口口口口口口口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
57 ['①②③④口①①＜口口口口口口口口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
58 ['③④⑤口⑥口①⑤⑦口⑤②①口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
59 ['口口口①口①①口口②②口②口口口', ['①ーーー', '②ーーー', 'ーーーー', 'ーーーー']]
60 ['③④⑤口⑥口口⑤⑦口⑤②①口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
61 ['口④④①③①①③③②②③②④④口', ['①ーーー', '②ーーー', '③ーーー', '④ーーー']]
62 ['⑤口⑦⑥口③口④⑤口②口口口口①', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
63 ['⑤⑤⑦口④⑦③⑦⑧②⑦口①口⑥⑥口口口口口口口口口口口口⑨口口口', ['①ー②ー', '③④ーー', '⑤ー⑥ー', '⑦ー⑧⑨']]
64 ['⑤③口④⑤口②⑥口口⑦①口口口口', ['①ー②ー', '③④ーー', '⑤ーー⑥', '⑦ーーー']]
65 ['口①①口③口口④③口口④口②②口', ['①ーーー②ー', 'ーー③ーーー', '④ーーー', 'ーーーー']]
66 ['口⑨⑤①⑦⑤③⑦⑩③⑥⑨①⑧②④⑪口口⑪口口口口口⑫口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
67 ['口口口口口②Ｖ＜口口口口口口①口口④口＜口口口③口口口口口口口∧口口口口口口口口口口口口⑥＞＜⑤', ['①ーーー②ー', 'ーー③ーーー', '④ーーー⑤ー', 'ーー⑥ーーー']]
68 ['口⑤口口口③口④口口口口口口②⑥⑤⑨⑦⑥⑦③④⑤①口①③①⑧②⑨口口口口口⑭⑮口⑩⑪⑫⑬口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩⑪⑫⑬⑭⑮']]
69 ['③⑥⑤③④口口②⑦口＜口①⑤①口口Ｖ口口口口口Ｖ口⑨口口口口口⑧', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ーーー⑧ー', 'ーー⑨ーーー']]
70 ['口口口口口口口口⑧口口口口口口⑨①⑤⑦⑤⑦⑨③①⑩①⑥④③⑧②⑨⑪口口口口口口⑪口⑫口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
71 ['⑨③⑥③⑤⑦①⑨口⑩④⑤①⑧②⑦口⑫口口口口⑪口⑪口口口口口口口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
72 ['⑦⑨③①⑧⑤⑩⑥口⑨②③⑤⑦①④口口口⑪口口口口口口⑪口口口⑫口', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
73 ['⑦⑪①⑩口③口⑥②⑨⑧④③⑤⑫①', ['①ー②ー③ー', '④ー⑤ー⑥ー', '⑦ー⑧ー⑨ー', '⑩ー⑪ー⑫ー']]
74 ['口⑪⑫口①②③④⑨⑧⑦⑥⑤⑬口⑩', ['①②③④', '⑤ー⑥⑦', '⑧⑨⑩ー', '⑪⑫ー⑬']]
75 ['口口口⑦⑥口口口口⑤④口②口①③', ['①ーーー', '②ーーー', '③④⑤⑥', '⑦ーーー']]
76 ['①口口口⑨②③⑧⑬⑩⑦④⑤⑥⑪⑫口口⑮⑯口⑭口口口口口口口口口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬⑭⑮⑯']]
77 ['③①口⑬⑥⑦⑧⑨口⑩⑤②④⑫⑪口', ['①②ー③', 'ー④ー⑤', '⑥⑦⑧⑨', '⑩⑪⑫⑬']]
78 ['②③①⑧口口⑨口口⑦⑤口⑥口口④⑩口口口口⑪口口口口口口口口口口', ['①ー②③', 'ー④⑤ー', '⑥⑦ー⑧', '⑨ー⑩⑪']]
79 ['⑪④⑤⑫口⑬⑩③②⑨⑧口⑦⑥①⑭', ['①②③④', '⑤⑥ー⑦', '⑧⑨⑩⑪', 'ー⑫⑬⑭']]
80 ['⑪①④⑫⑤⑮⑭⑧⑬⑨⑩②⑦③⑥⑯口⑰⑳口口口口口口口口⑱口⑲口口', ['①②③④', '⑤⑥⑦⑧', '⑨⑩⑪⑫', '⑬⑭⑮⑯⑰⑱⑲⑳']]
81 ['口口口口①口口口口口口口口口口口', ['①ーーー', 'ーーーー', 'ーーーー', 'ーーーー']]
```
