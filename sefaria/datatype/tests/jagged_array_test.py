# -*- coding: utf-8 -*-

import sefaria.datatype.jagged_array as ja


def setup_module(module):
    global twoby, threeby, two_by_mask
    twoby = [
                ["Line 1:1", "This is the first second", "First third"],
                ["Chapter 2, Verse 1", "2:2", "2:3"],
                ["Third first", "Third second", "Third third"]
    ]
    two_by_mask = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    threeby = [
        [
            ["Part 1 Line 1:1", "This is the first second", "First third"],
            ["Chapter 2, Verse 1", "2:2", "2:3"],
            ["Third first", "Third second", "Third third"]
        ],
        [
            ["Part 2 Line 1:1", "This is the first second", "First third"],
            ["Chapter 2, Verse 1", "2:2", "2:3"],
            ["Third first", "Third second", "Third third"]
        ],
        [
            ["Part 3 Line 1:1", "This is the first second", "First third"],
            ["Chapter 2, Verse 1", "2:2", "2:3"],
            ["Third first", "Third second", "Third third"]
        ],
    ]


class Test_Jagged_Text_Array(object):

    def test_count_words(self):
        assert ja.JaggedTextArray(twoby).word_count() == 21
        assert ja.JaggedTextArray(threeby).word_count() == 69


    def test_count_chars(self):
        assert ja.JaggedTextArray(twoby).char_count() == 101
        assert ja.JaggedTextArray(threeby).char_count() == 324

    def test_verse_count(self):
        assert ja.JaggedTextArray(twoby).verse_count() == 9
        assert ja.JaggedTextArray(threeby).verse_count() == 27

    def test_equality(self):
        assert ja.JaggedTextArray(twoby) == ja.JaggedTextArray(twoby)
        assert ja.JaggedTextArray(threeby) == ja.JaggedTextArray(threeby)
        assert ja.JaggedTextArray(twoby) != ja.JaggedTextArray(threeby)

    def test_subarray(self):
        assert ja.JaggedTextArray(threeby).subarray([0],[0]) == ja.JaggedTextArray([
            ["Part 1 Line 1:1", "This is the first second", "First third"],
            ["Chapter 2, Verse 1", "2:2", "2:3"],
            ["Third first", "Third second", "Third third"]
        ])
        assert ja.JaggedTextArray(threeby).subarray([1],[1]) == ja.JaggedTextArray([
            ["Part 2 Line 1:1", "This is the first second", "First third"],
            ["Chapter 2, Verse 1", "2:2", "2:3"],
            ["Third first", "Third second", "Third third"]
        ])
        assert ja.JaggedTextArray(threeby).subarray([1,1,1],[1,2,1]) == ja.JaggedTextArray([
            ["2:2", "2:3"],
            ["Third first", "Third second"]
        ])

    def test_set_element(self):
        j = ja.JaggedTextArray(twoby).set_element([1,1], "Foobar")
        assert j.get_element([1, 1]) == "Foobar"
        assert j.array() == [
                ["Line 1:1", "This is the first second", "First third"],
                ["Chapter 2, Verse 1", "Foobar", "2:3"],
                ["Third first", "Third second", "Third third"]
        ]
        j = ja.JaggedTextArray(twoby).set_element([1], ["Foobar", "Flan", "Bob"])
        assert j.get_element([1]) == ["Foobar", "Flan", "Bob"]
        assert j.array() == [
                ["Line 1:1", "This is the first second", "First third"],
                ["Foobar", "Flan", "Bob"],
                ["Third first", "Third second", "Third third"]
        ]
        j = ja.JaggedTextArray()
        assert j.set_element([2, 3], "Foo").array() == [
            [],
            [],
            [None, None, None, "Foo"]
        ]

    def test_mask(self):
        assert ja.JaggedTextArray(twoby).mask() == ja.JaggedIntArray(two_by_mask)
        assert ja.JaggedTextArray(
            [
                ["a",[],[],["",""],["b"]],
                ["a",[],["","a"],["",""],["b"]]
            ]
        ).mask() == ja.JaggedIntArray(
            [
                [1,[],[],[0,0],[1]],
                [1,[],[0,1],[0,0],[1]]
            ]
        )

        assert ja.JaggedTextArray(
            [
                ["a",[],[],["",""],["b"]],
                ["a",[],["","a"],["",""],["b"]]
            ]
        ).zero_mask() == ja.JaggedIntArray(
            [
                [0,[],[],[0,0],[0]],
                [0,[],[0,0],[0,0],[0]]
            ]
        )

        assert ja.JaggedTextArray(
            [
                ["a",[],[],["",""],["b"]],
                ["a",[],["","a"],["",""],["b"]]
            ]
        ).constant_mask(None) == ja.JaggedIntArray(
            [
                [None,[],[],[None,None],[None]],
                [None,[],[None,None],[None,None],[None]]
            ]
        )

    def test_is_full(self):
        assert ja.JaggedTextArray(twoby).is_full()
        assert ja.JaggedTextArray(threeby).is_full()
        assert not ja.JaggedTextArray([]).is_full()
        assert not ja.JaggedTextArray([[]]).is_full()
        assert not ja.JaggedTextArray([[""]]).is_full()
        assert not ja.JaggedTextArray([["a","b","c",""]]).is_full()
        assert not ja.JaggedTextArray([["a","b","c",[""]]]).is_full()

    def test_is_empty(self):
        assert not ja.JaggedTextArray(twoby).is_empty()
        assert not ja.JaggedTextArray(threeby).is_empty()
        assert ja.JaggedTextArray([]).is_empty()
        assert ja.JaggedTextArray([[]]).is_empty()
        assert ja.JaggedTextArray([[""]]).is_empty()
        assert not ja.JaggedTextArray([["a","b","c",""]]).is_empty()
        assert not ja.JaggedTextArray([["a","b","c",[""]]]).is_empty()

    def test_sections(self):
        assert ja.JaggedTextArray(twoby).sections() == [[0],[1],[2]]
        assert ja.JaggedTextArray(threeby).sections() == [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

    def test_trim_ending_whitespace(self):
        #do no harm
        assert ja.JaggedTextArray(twoby).trim_ending_whitespace() == ja.JaggedTextArray(twoby)
        assert ja.JaggedTextArray(threeby).trim_ending_whitespace() == ja.JaggedTextArray(threeby)

        twoby_with_space = [
            ["Line 1:1", "This is the first second", "First third","","",""],
            ["Chapter 2, Verse 1", "2:2", "2:3", ""],
            ["Third first", "Third second", "Third third"]
        ]
        threeby_with_space = [
            [
                ["Part 1 Line 1:1", "This is the first second", "First third","","",""],
                ["Chapter 2, Verse 1", "2:2", "2:3", "", ""],
                ["Third first", "Third second", "Third third",""]
            ],
            [
                ["Part 2 Line 1:1", "This is the first second", "First third"],
                ["Chapter 2, Verse 1", "2:2", "2:3","","",""],
                ["Third first", "Third second", "Third third"]
            ],
            [
                ["Part 3 Line 1:1", "This is the first second", "First third"],
                ["Chapter 2, Verse 1", "2:2", "2:3"],
                ["Third first", "Third second", "Third third",""]
            ],
        ]
        assert ja.JaggedTextArray(["a","b","c","",""]).trim_ending_whitespace() == ja.JaggedTextArray(["a","b","c"])
        assert ja.JaggedTextArray(twoby_with_space).trim_ending_whitespace() == ja.JaggedTextArray(twoby)
        assert ja.JaggedTextArray(threeby_with_space).trim_ending_whitespace() == ja.JaggedTextArray(threeby)

    def test_overlap(self):
        a = ja.JaggedTextArray([["","b",""],["d","","f"],["","h",""]])
        b = ja.JaggedTextArray([["","","c"],["","e",""],["g","",""]])
        c = ja.JaggedTextArray([["","",""],["","q",""],["","",""]])
        assert not a.overlaps(b)
        assert not a.overlaps(c)
        assert b.overlaps(c)

    def test_resize(self):
        assert ja.JaggedTextArray(twoby).resize(1).resize(-1) == ja.JaggedTextArray(twoby)

    def test_flatten(self):
        assert ja.JaggedTextArray(threeby).flatten_to_array() == [
            "Part 1 Line 1:1", "This is the first second", "First third",
            "Chapter 2, Verse 1", "2:2", "2:3",
            "Third first", "Third second", "Third third",
            "Part 2 Line 1:1", "This is the first second", "First third",
            "Chapter 2, Verse 1", "2:2", "2:3",
            "Third first", "Third second", "Third third",
            "Part 3 Line 1:1", "This is the first second", "First third",
            "Chapter 2, Verse 1", "2:2", "2:3",
            "Third first", "Third second", "Third third"
        ]



class Test_Depth_0(object):
    def test_depth_0(self):
        j = ja.JaggedTextArray("Fee Fi Fo Fum")
        assert j._store == "Fee Fi Fo Fum"
        assert j.is_full()
        assert not j.is_empty()
        assert j.verse_count() == 1
        assert j.mask() == ja.JaggedIntArray(1)
        assert j.flatten_to_array() == "Fee Fi Fo Fum"

