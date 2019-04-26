#keeping my helper functions out of main.py for a cleaner, more tidy code (winky eye!)


def is_email(string):
    '''
    is_email(<takes an email as a string>)
        returns FALSE if @ not present
        returns _____ if domainDot is present
    Verifies whether or not an email is valid.
    '''
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present