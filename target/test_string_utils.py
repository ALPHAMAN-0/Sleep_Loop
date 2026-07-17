from string_utils import slugify


def test_basic():
    assert slugify("Hello World") == "hello-world"


def test_strip_whitespace():
    assert slugify("  Hello World  ") == "hello-world"


def test_underscores_and_spaces():
    assert slugify("hello_world  again") == "hello-world-again"


def test_drops_punctuation():
    assert slugify("Hello, World!") == "hello-world"


def test_collapses_hyphens():
    assert slugify("a---b   c") == "a-b-c"


def test_no_edge_hyphens():
    assert slugify("!!Hello!!") == "hello"
