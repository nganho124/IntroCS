words = set()

def check(word):
    """Check if a word is in the set of words."""
    return word.lower() in words

def load(dictionary):
    with open(dictionary) as f:
        words.update(file.read().splitlines())
    return True

def size():
    return len(words)

def unload():
    return True
