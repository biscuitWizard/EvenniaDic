import random


def progress_bar(value, max_value, width=20, display="multicolor"):
    """
    Renders a progress bar in ASCII.
    Args:
        value       (int): Current progress value
        max_value   (int): Max possible progress value
        width       (int, optional): The width of the bar, in characters.
        display     (str, optional): How the bar will be colored.
    Returns:
        text (str): The progress bar.
    """
    if width < 2:
        return
    percentile = 0
    if max_value > 0:
        percentile = value / max_value

    text = "["
    bars = width - 2
    index = 0
    while index < bars:
        if index / bars >= percentile:
            text += " "
        else:
            color = get_segment_color(index / bars, display)
            text += "%s|||n" % color
        index += 1
    text += "]"
    return text


def get_segment_color(percentile, display):
    if display == "multicolor":
        if percentile < 0.1:
            return "|r"
        elif percentile < 0.6:
            return "|y"
        else:
            return "|g"
    elif display == "multicolor-inverse":
        if percentile < 0.4:
            return "|g"
        elif percentile < 0.9:
            return "|y"
        else:
            return "|r"
    return "|n"


def corrupt(text, probability):
    charset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-"
    index = 0
    result = ""
    while index < len(text):
        if text[index] == '|' or (index > 0 and text[index] == '|'):
            # don't fuck with ansi.
            result += text[index]
        elif random.randint(1,100) < probability:
            result += charset[random.randint(1, len(charset) - 1)]
        else:
            result += text[index]
        index += 1

    return result