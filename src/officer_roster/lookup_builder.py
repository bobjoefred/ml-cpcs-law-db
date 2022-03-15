"""Pandas module via modin speedup"""
import pandas as pd

class Officers:
    """Officers module to provide lookup functionality"""
    def __init__(self):
        self.data = pd.read_csv("officer_roster/data/officer_roster.csv")

    def lookup(self, first_name, last_name):
        """
        This method takes in the first name and last name of the officer,
        returning the whole entry
        """
        return self.data["Internal Unique ID"][
            (self.data['First Name'] == first_name.lower()) &
            (self.data['Last Name'] == last_name.lower())].to_string(index=False)

def get_officer_client():
    """
    Get officer client
    """
    return Officers()
