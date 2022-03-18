"""Import officer lookup dependency"""
import officer_roster.lookup_builder as lookup

client = lookup.get_officer_client()
result = client.lookup("Anderson", "Paul")
print(result)

