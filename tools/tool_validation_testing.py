
def run(user_input):
    if isinstance(user_input, str):
        if len(user_input) >= 5:
            return True
        else:
            return False
    else:
        return False
