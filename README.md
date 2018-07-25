# Auto_Summarization_Tool
Implementing an Automatic Text Summarization Tool, using Python3 and also with the help of 2 research papers.

Summarization of text documents or articles can be done using 2 approaches:
1. Statistical Approach
2. Linguistic Approach

The **Linguistic Approach** is similar to human based approach for generating summaries of large documents, or articles.It is quite abstract way to generate summary and relies heavily on Natural Language Processing(NLP).Involves determining parts of speech and involves sentence formation.
The **Statistical Approach** involves use of word frequency, sentence scores, and even some graph based approach to determine what are the most relevant sentences in the given article.

Following is a list of Python Libraries that are used:

* numpy
* matplotlib
* wikipedia
* networkx
* re
* nltk
* collections- defaultdict


In this project, i am using **Statistical Approach**. The whole program is basically divided into 4 modules/Classes where each class performs a specific task.

* Title_Selector :- Get the title of the article from the user, about which they would like to generate the summary.After the    user has entered their choice, ask the user to enter the id number of the article they would like to get summarized.
* Content_Fetcher :- Fetch the content of the corresponding article from wikipedia, and perform some cleaning on the data, with  the data with the help of regular expression.
* Text_Cleaner :- This class performs jaccard similarity for each pair of paragraphs, to determine the highly similar     paragraphs.
* Generate_Similarity_Graph :- This class is used to generate a similarity graph.Each paragraph denoted as a node, and if there exists a similarity between the two paragraphs which is greater than the threshold value, then the two nodes are connected by an edge.

When the function _main()_ is called, due to herarichal inheritence, the topmost class _init()_ method is invoked, and each class init() method is invoked sequentially.During the execution of the program if an error occours, then the program terminates, with a prompt asking the user for choice whether, the user wants to enter the value again or not.

Besides all these implementation details, this project heavily relies on two research papers:
1. [Automatic Text Summarization by paragraph Extraction
    Mandar Mitrat~'Amit Singhalt, Chris Buckley tt ](http://www.aclweb.org/anthology/W97-0707)    
    
2. [LexRank:Graph-basedLexicalCentrality as SalienceinText Summarization
   Gunes Erkan DragomirR.Radev](https://www.jair.org/index.php/jair/article/view/10396/24901)
   
Please share your insights and any assistance by you that contributes to the development of this project will be highly appreciated.
