---
description: GENERATING FAMILY TREE USING GRAPHVIZ
cover: .gitbook/assets/family_tree-8.png
coverY: 250
layout:
  cover:
    visible: true
    size: full
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# 😀 Page 2

{% embed url="https://www.youtube.com/watch?v=_iPPdFdLM3M" %}

{% code title="" lineNumbers="true" fullWidth="false" %}
````markdown

```python
// Import the required libraries
import pandas as pd
import graphviz
import colorsys
import random

# Read the family tree data from a CSV file
df = pd.read_csv('family_tree_data.csv')

# Create different color blocks for each clan
clans = list(df['clan'].unique())
colors = {}
for i in clans:
    hue = i / len(clans)
    rgb = colorsys.hsv_to_rgb(hue, 0.4, 1)
    rgb_int = [int(c * 255) for c in rgb]
    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_int)
    colors[i] = hex_color

# Read the clan names from a text file
with open('clan_names.txt', 'r') as file:
    content = file.readlines()

clan_names = [line.strip() for line in content]
clans_dict = {}
for i in clans:
    selected = random.choice(clan_names)
    clans_dict[i] = selected
    clan_names.remove(selected)

# Create the family graph using Graphviz
graph = graphviz.Graph(engine='dot', format='png')
graph.attr(rankdir='TB')

node_attributes = {
    'fontname': 'Arial',
}

# Iterate over the family tree data to create nodes
for _, row in df.iterrows():
    node_id = str(row['#pid'])
    node_label = f"{row['name']}\n[{row['byear']} - {row['dyear']}]\nage: {row['dage']} {row['gender'][0]}\nclan: {clans_dict[row['clan']]}"

    # Set the node shape based on gender
    if row['gender'] == 'Male':
        node_attributes['shape'] = 'rectangle'
    else:
        node_attributes['shape'] = 'oval'

    # Add the node to the graph
    graph.node(node_id, label=node_label, style='filled', fillcolor=colors[row['clan']], **node_attributes)

# Add edges between spouses
for _, row in df.iterrows():
    spouse_id = row['spouseId']
    if pd.notna(spouse_id):
        graph.edge(str(row['#pid']), str(int(spouse_id)), color='red')

# Add edges between parents and children
for _, row in df.iterrows():
    parent_id1 = row['parentId1']
    parent_id2 = row['parentId2']
    if pd.notna(parent_id1):
        graph.edge(str(int(parent_id1)), str(row['#pid']), dir='none', color='black')

# Set additional graph attributes
graph.attr(ranksep='1.5')

# Save the graph as a DOT file
graph.save('family_tree.dot')

# Render the graph as a PNG image
graph.render('family_tree', format='png', view=True)

````
{% endcode %}
