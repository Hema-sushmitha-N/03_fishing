"""
catch: hook-vs-fish catch detection.
"""


def check_catch(hook, fish_list):
    """
    Returns the fish the hook has caught, or None.
    """
    for fish in fish_list:
        if abs(hook.y - fish.y) < 10:
            return fish
    return None
