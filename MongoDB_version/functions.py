def is_number(number):
    if isinstance(number, int):
        if number >= 0:
            return True
        else:
            return False
    elif isinstance(number, str):
        if number.isdigit() == True:
            return True
        else:
            return False
    else:
        return False