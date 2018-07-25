import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import wikipedia as wp
import re
import os

from nltk.corpus import stopwords as swords

from collections import defaultdict

# provides user with the flexiblity to enter the title and get its content summarized
class Title_Selector():
    def __init__(self):
        self.keyword = None
        self.cond =True                                           # condition variable
        self.topic_index = None                                   # index of topic of interest
        self.titles = None                                        # list of all the similar titles
        self.indexed_titles = None                                # list of topics with indexed titles
    # method to generate a list of similar titles and asking the user to input their choice
    def get_title(self):
        try:
            while self.cond:
                print("============================================================================================")
                print('Enter the title of the content or a similar keyword which you want to summarize')
                print('--->',end=' ')
                self.keyword = input()
                self.titles = wp.search(self.keyword,results=20)                   # search for all the similar titles
                if len(self.titles) > 1:
                    self.indexed_titles = list(enumerate(self.titles))
                    for i,j in enumerate(self.titles,1):                      # print list of titles with index value
                        print(i,j)
                    cond1 = True
                    while cond1:                                              # asking for id number for topic of interest
                        print('  Enter the Id number of the topic that seems relevant to you')
                        print('  --->',end=' ')
                        self.topic_index = input()
                        try:
                            print('  Fetching text content about ',self.titles[int(self.topic_index)-1])
                            self.cond = False
                            cond1 = False
                        except:
                            print('  ============================================================================================')
                            print('  Index Not in range!')
                            print('  Want to re-enter the index')
                            print("  Enter '1' for yes and \n '0' for no")
                            choice = int(input())                             # if choice is 0 then exit
                            if choice == 1:
                                cond1 = True
                            else:
                                self.cond = False
                                cond1 = False
                                self.end()                            # if self.end() contains exit(), then above two lines not relevant

                else:
                    print('No related articles found for the given topic !')                  # when user enters sophisticated keyword
                    print('==========================================================================================')
                    print('Do you want to retry?')
                    print("Enter '1' for yes and \n '0' for no")
                    choice = int(input())
                    if choice == 1:
                        self.cond = True
                    elif choice == 0:
                        self.cond = False
                        self.topic_index = None
                        self.titles = None
                        self.indexed_titles = None
                        print('Program Halts !')
            return self.indexed_titles[int(self.topic_index)-1] if self.indexed_titles else None
        except:
            self.end()

    def end(self):
        exit()



# =============================================================================
#
# =============================================================================


class Content_Fetcher(Title_Selector):
    def __init__(self):
        try:
            super().__init__()
            self.topic = super().get_title()
            self.page = None
            self.content = None
            self.formatted_content = None
            self.paragraphs = None
        except:
            self.end()

    def show(self):
        try:
            self.page = wp.page(self.topic[1])
            self.content = self.page.content
            self.content = self.content.lower()
            self.formatted_content, _ = re.subn(r"\n{2,3}={2,3}.?[-'0-9a-zA-Z)( ]+.?={2,3}\n{2,3}",'*******%*?*#*&******',self.content)
            self.paragraphs = np.array(self.formatted_content.split('*******%*?*#*&******'))
            return self.paragraphs
        except wp.exceptions.DisambiguationError:
            print('The keyword is quite ambiguous, please be more specific')
            print('Want to retry?, 0 for no \n 1 for yes')
            choice = int(input())
            if choice == 0:
                self.end()
            else:
                self.__init__()
        except:
            None
    def end(self):
        Title_Selector.end(self)

# =============================================================================
#
# =============================================================================


class Text_Cleaner(Content_Fetcher,Title_Selector):
    def __init__(self):
        try:
            super().__init__()
            self.pars = super().show()
            self.n = len(self.pars)
        except:
            self.end()

    def cleaning(self):
        try:
            jacard_similarity = np.zeros((self.n,self.n))               ##### use numpy here to create a 2d array
            stop_free_pars = []
            stopwords = swords.words('english')
            for paragraph in self.pars:
                stop_free_pars.append([word for word in paragraph if word not in stopwords])
            for parai in range(self.n):
                for paraj in range(self.n):
                    if parai != paraj:
                        seti = set(stop_free_pars[parai])
                        setj = set(stop_free_pars[paraj])
                        jacard_similarity[parai][paraj] = len(seti.intersection(setj))/len(seti.union(setj))
            return jacard_similarity,np.amax(jacard_similarity)
        except:
            self.end()

    def end(self):
        Title_Selector.end(self)

# =============================================================================
#
# =============================================================================


class Generate_Similarity_Graph(Text_Cleaner,Title_Selector):
    def __init__(self):
        try:
            super().__init__()
            self.sim_score, self.max_score = super().cleaning()
            self.G = nx.Graph()
            self.relevant_nodes = None
            self.temp = None
        except:
            self.end()

    def generate_graph(self):
        try:
    #         thresh_percent = [i for i in np.linspace(0.1,0.9,num=9)]
    #         for percent in thresh_percent:
            plt.figure()
            self.temp = np.where(self.sim_score<0.90*self.max_score,0,1)
            self.G.add_edges_from([(i,j) for i in range(len(self.sim_score[0])) for j in range(len(self.sim_score[0])) if self.temp[i][j] == 1])
            node_sizes = np.array([(300*i*2) for i in nx.degree_centrality(self.G).values()])
            plt.title('Graph depicting relevance of each paragraph')
            nx.draw_circular(self.G,with_labels=True,node_size = node_sizes,cmap = plt.cm.gray)
            plt.show()
        except:
            self.end()

    def generate_degree_count(self):
        x = list(self.G.nodes)
        y = dict(nx.degree(xx.G,nbunch=xx.G.nodes)).values()
        plt.figure()
        plt.scatter(x,y)
        plt.xlabel('Paragraph ID')
        plt.ylabel('No. of Connections')
        plt.title('Total connections for each paragraph',loc='center')
        plt.show()

    def extract_relevant_nodes(self):
        self.relevant_nodes = defaultdict(int)
        for i in range(len(self.temp)):
            for j in range(len(self.temp[i])):
                if self.temp[i][j] == 1:
                    self.relevant_nodes[i]+=1
                    self.relevant_nodes[j]+=1
        self.relevant_nodes = dict(sorted(self.relevant_nodes.items(),key=lambda x: x[1],reverse=True))
        max_degree_node = sorted(self.relevant_nodes.items(),key=lambda x: x[1],reverse=True)[0][0]
        self.relevant_nodes = dict([(i,j) for i,j in self.relevant_nodes.items() if j >= self.relevant_nodes[max_degree_node]//2 ])
        return  list(self.relevant_nodes.keys())


    def end(self):
        Title_Selector.end(self)

# =============================================================================
#
# =============================================================================


def position_score():
    obj = Generate_Similarity_Graph()
    obj.generate_graph()
    paras = obj.paragraphs[obj.extract_relevant_nodes()]
    doc = '.'.join(i for i in paras)
    doc, _= re.subn(r"[^,'.%$a-zA-Z0-9]",' ',doc)
    indexed_sentence = np.array(list(enumerate(doc.split('.'),0)))
#     position_score = [1/i**0.5 for i,_ in indexed_sentence]
    words = []
    for i in range(len(indexed_sentence)):
        words.append([word for word in indexed_sentence[i][1].split(' ') if word not in swords.words('english')])
#     print(words)
    sentence_similarity = np.zeros((len(words),len(words)))
    for i in range(len(words)):
        for j in range(len(words)):
            if i!=j:
                senti = set(words[i])
                sentj = set(words[j])
                if len(senti) != 0 and len(sentj) != 0:
                    sentence_similarity[i][j] = len(senti.intersection(sentj))/len(senti.union(sentj))
    max_score_sentences_row = sentence_similarity.argmax(axis=1)
    max_score_sentences_col = sentence_similarity.argmax(axis=0)
    commen_sentences = set(max_score_sentences_row).intersection(max_score_sentences_col)

    graph = nx.Graph()
    graph.add_edges_from([(i,j) for i in max_score_sentences_row for j in max_score_sentences_col
                          if i in commen_sentences and j in commen_sentences])
    sizes = np.array([30*i*2 for i in nx.degree_centrality(graph).values()])
    plt.figure()
    plt.title('Graph depicting relevance of each sentence')
    nx.draw_circular(graph,node_size=sizes)
    plt.show()

#     deleteit = np.amax(sentence_similarity,axis=0)
#     print(len(deleteit[deleteit>0.2]))


#     for i in range(10,20):
#         plt.figure()
#         plt.plot(sentence_similarity[i])
#         plt.show()


#     sentence_similarity = np.where((sentence_similarity > 0.02) &(sentence_similarity < 0.06),1,0)
#     sentence_similarity = np.where(sentence_similarity > 0.124,1,0)
#     G_sentences = nx.Graph()
#     G_sentences.add_edges_from([(i,j) for i in range(len(sentence_similarity[0])) for j in range(len(sentence_similarity[0]))
#                                                        if sentence_similarity[i][j]== 1])
#     plt.figure()
#     node_sizes = np.array([(300*i*2) for i in nx.degree_centrality(G_sentences).values()])
#     nx.draw_networkx(G_sentences,node_size=node_sizes)
#     plt.show()

#     summary_sentences_indices = list(sorted(nx.connected_components(G_sentences),key=len,reverse=True))[0]

    summary = '.\n'.join(re.sub(r' +',' ',indexed_sentence[i][1]).strip().capitalize()
                                  for i in sorted(set(commen_sentences))[:40] if len(indexed_sentence[i][1]) > 10)

    with open('summary.temp','a+') as f:
        f.writelines(summary)

    print('Summary saved to the text file at location ',os.path.abspath('.'))
#     print(summary_sentences_indices)


position_score()