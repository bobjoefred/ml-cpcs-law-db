def lookup(name, agency, data):
    """
    This method takes in the first name and last name of the officer,
    returning the whole entry
    """
    split_name = name.split(' ')
    first_name = split_name[0]
    last_name = split_name[1]
    result = data[
        (data['First Name'] == first_name.lower()) &
        (data['Last Name'] == last_name.lower())]

    if result.empty:
        return None
    elif result.shape[0] == 1:
        return result['Internal Unique ID'].to_string(index=False)
    else:
        # in the case of multiple people with the same name, also search by agency
        if agency:
            officer_agency = result[result['Agency'] == agency.split(' ')[0]]
            return None if officer_agency.empty else officer_agency['Internal Unique ID'].to_string(index=False)
    return None