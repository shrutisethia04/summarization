
# coding: utf-8

# In[56]:

import pickle
import pandas as pd
import matplotlib.pyplot as plt




# In[70]:

class comparison:
	def __init__(self,hashtag):
		self.hashtag= hashtag
		self.df_cluster= ''
		self.df_hyd= ''
		self.df_retweet= ''
		
		data= pickle.load( open( 'pkl_files/'+self.hashtag+'_cluster.pkl', "rb" ) )
		self.df_cluster= pd.DataFrame(data)

		data= pickle.load( open( 'pkl_files/'+self.hashtag+'_hyd.pkl', "rb" ) )
		self.df_hyd= pd.DataFrame(data)
		# index=['file', 'skip_bigrams_stats','lcs_score','unigram_precision','bigram_precision','trigram_precision','unigram_recall','bigram_recall','trigram_recall', 'unigram', 'bigram', 'trigram'])
		data= pickle.load( open( 'pkl_files/'+self.hashtag+'_retweet.pkl', "rb" ) )
		self.df_retweet= pd.DataFrame(data)
		# print self.df_retweet
        
   
	def compare(self):
		df= pd.concat([self.df_cluster, self.df_hyd,self.df_retweet],axis=0, keys=['Cluster TFIDF', 'Hyd TFIDF', 'Retweet'])
		# print "df crreated"
		# print df
		return df

	def comparison_plot(parameter):    
		fig = plt.figure(figsize=(6,6))
		sub1 = fig.add_subplot(421) # instead of plt.subplot(2, 2, 1)
		sub1.set_title('Cluster TF-IDF') # non OOP: plt.title('The function f')
		sub1.boxplot(self_df_cluster[parameter] )
		sub2 = fig.add_subplot(422) # instead of plt.subplot(2, 2, 1)
		sub2.boxplot(self.df_hyd[parameter])
		sub2.set_title('Hybd TF-IDF')
		sub3 = fig.add_subplot(423) # instead of plt.subplot(2, 2, 1)
		sub3.boxplot(self.df_retweet[parameter])
		sub3.set_title('Retweet')
		plt.tight_layout()
		plt.show()



# In[74]:

p= comparison('uspresidentialelections')
p.compare()

