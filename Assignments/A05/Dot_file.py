import pandas as pd
import graphviz
import colorsys
import random

df = pd.read_csv('family_tree_data.csv')

# create differnt color blocks for each clan

clans = list(df[' clan'].unique())
colors = {}
for i in clans:
    hue = i/len(clans)
    rgb = colorsys.hsv_to_rgb(hue, 0.4, 1)
    rgb_int = [int(c * 255) for c in rgb]
    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_int)
    colors[i] = hex_color

with open('clan_names.txt', 'r') as file:
    content = file.readlines()

clan_names = [line.strip() for line in content]
clans_dict = {}
for i in clans:
    selected = random.choice(clan_names)
    clans_dict[i] = selected
    clan_names.remove(selected)

# creating the family graph
graph = graphviz.Graph(engine='dot', format='png')
graph.attr(rankdir='TB')

node_attributes = {
    'fontname': 'Arial',
}
    
for _, row in df.iterrows():
    node_id = str(row['#pid'])
    node_label = f"{row[' name']}\n[{row[' byear']} - {row[' dyear']}]\nage: {row[' dage']} {row[' gender'][0]}\nclan: {clans_dict[row[' clan']]}"     
    
    if row[' gender'] == 'Male':
        node_attributes['shape'] = 'rectangle' #using rectangular shape for male
    else:
        node_attributes['shape'] = 'oval'#Oval shape for female
    graph.node(node_id, label=node_label, style='filled', fillcolor=colors[row[' clan']], **node_attributes) 

for _, row in df.iterrows():# Creating red colour edges betwen spouse
    spouse_id = row[' spouseId']
    if pd.notna(spouse_id):
        graph.edge(str(row['#pid']), str(int(spouse_id)), color='red')

for _, row in df.iterrows():# Creating red colour edges between spouse
    parent_id1 = row[' parentId1']
    parent_id2 = row[' parentId2']
    if pd.notna(parent_id1):
        graph.edge(str(int(parent_id1)), str(row['#pid']), dir='none', color='black', )

graph.attr(ranksep='1.5')

graph.save('family_tree.dot')

graph.render('family_tree', format='png', view=True)
