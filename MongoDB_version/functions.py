def is_number(number):
    if isinstance(number, int):
        if number >= 0:
            return True
        else:
            return False
    number = str(number)
    if number.isdigit() == True:
        return True
    else:
        return False