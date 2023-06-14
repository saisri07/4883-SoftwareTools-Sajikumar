import pandas as pd

df = pd.read_csv('tree.csv')
df2 = pd.read_csv('mock_names.csv')

mapping = {'F': 'Female', 'M': 'Male'} #mapping Female for F and Male for M
df[' gender'] = df[' gender'].map(mapping)

# For each name in the generated data, first_name of mock_names are mapped
matching_dict = {} 
for index, row in df.iterrows():
    gender = row[' gender']
    match = df2[df2['gender'] == gender]
    if not match.empty:
        available_names = set(match['first_name']).difference(matching_dict.values())
        if len(available_names) > 0:
            matching_dict[row[' name']] = available_names.pop()

df[' name'] = df[' name'].map(matching_dict) #mapping the names
df.to_csv('family_tree_data.csv', index=False) # saving the edited data
