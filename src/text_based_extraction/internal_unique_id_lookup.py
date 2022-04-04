def lookup(name, data):
    """
    This method takes in the first name and last name of the officer,
    returning the whole entry
    """
    split_name = name.split(' ')
    first_name = split_name[0]
    last_name = split_name[1]
    result = data["Internal Unique ID"][
        (data['First Name'] == first_name.lower()) &
        (data['Last Name'] == last_name.lower())]
    return None if result.empty else result.to_string(index=False)