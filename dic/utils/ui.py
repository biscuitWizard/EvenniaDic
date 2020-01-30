def progress_bar(value, max, width=20, display="multicolor"):
    """
    Renders a progress bar in ASCII.
    Args:
        value (int): Current progress value
        max   (int): Max possible progress value
        width (int, optional): The width of the bar, in characters.
        display(str, optional): How the bar will be colored.
    Returns:
        text (str): The progress bar.
    """
    if width < 2:
        return
    percentile = 0
    if max > 0:
        percentile = value / max

    text = "["
    bars = width - 2
    index = 0
    while index < bars:
        if index / bars >= percentile:
            text += " "
        else:
            color = get_segment_color(percentile, display)
            text += "%s#|n" % color
        index += 1
    text += "]"
    return text


def get_segment_color(percentile, display):
    if display == "multicolor":
        if percentile < 0.3:
            return "|r"
        elif percentile < 0.6:
            return "|y"
        else:
            return "|g"
    elif display == "multicolor-inverse":
        if percentile < 0.4:
            return "|g"
        elif percentile < 0.7:
            return "|y"
        else:
            return "|r"
    return "|n"
