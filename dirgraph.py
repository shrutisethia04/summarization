import networkx as nx
import string
from sys import maxint

str1 = """ 
"""
tweets= ['31 year old Seth Foti was carrying pouches containing classified information.', 'The american killed in the crash was 31 year old Seth J Foti, a diplomatic courier carrying classified documents.']
#tweets = tweets.split(None)
dG = nx.DiGraph()
dG.add_node('START')
dG.node['START']['count'] = 0
dG.add_node('END')
dG.node['END']['count'] = 0

for tweet in tweets:
	tweet = tweet.split() 
	tweet=[string.rstrip(x.lower(), ',.!?;') for x in tweet]
	print tweet
#wordList2 = [string.rstrip(x.lower(), ',.!?;') for x in tweets]
#print wordList2
	n= len(tweet)
	print tweet[n-1]
	
	for i, word in enumerate(tweet):
		print i, word

		try:
			if i==n-1:
				if not dG.has_edge(word, 'END'):
			 		dG.add_edge(word,'END', weight =maxint-1)
			 	else:
			 		dG.edge[word]['END']['weight']+=1
			 	dG.node['END']['count'] -=1
			
			next_word = tweet[i + 1]
			if not dG.has_node(word):
			    dG.add_node(word)
			    dG.node[word]['count'] = 1

			else:
			    dG.node[word]['count'] += 1

			if not dG.has_node(next_word):
			    dG.add_node(next_word)
			    dG.node[next_word]['count'] = 0

			if not dG.has_edge(word, next_word):
			    dG.add_edge(word, next_word, weight=maxint - 1)
			else:
			    dG.edge[word][next_word]['weight'] -= 1

			if i==0:
			 	if not dG.has_edge('START', word):
			 		dG.add_edge('START', word, weight =maxint-1)
			 	else:
			 		dG.edge['START'][word]['weight']-=1
			 	dG.node['START']['count'] +=1

			
			    
		except IndexError:
			if not dG.has_node(word):
			    dG.add_node(word)
			    dG.node[word]['count'] = 1
			else:
			    dG.node[word]['count'] += 1
		except:
			raise

	
	for node in dG.nodes():
	    print '%s:%d\n' % (node, dG.node[node]['count'])

	for edge in dG.edges():
	    print '%s:%d\n' % (edge, maxint - dG.edge[edge[0]][edge[1]]['weight'])
	
shortest_path = nx.shortest_path(dG, source='START', target='END', weight='weight')
print shortest_path