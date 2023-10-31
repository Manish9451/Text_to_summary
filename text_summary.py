import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# text="""While conventional search engines ranked results by counting how many times the search terms appeared on the page, they theorized about a better system that analyzed the relationships among websites.[27] They called this algorithm PageRank; it determined a website's relevance by the number of pages, and the importance of those pages that linked back to the original site.[28][29] Page told his ideas to Hassan, who began writing the code to implement Page's ideas.[23]

# Page and Brin originally nicknamed the new search engine "BackRub", because the system checked backlinks to estimate the importance of a site.[20][30][31] Hassan as well as Alan Steremberg were cited by Page and Brin as being critical to the development of Google. Rajeev Motwani and Terry Winograd later co-authored with Page and Brin the first paper about the project, describing PageRank and the initial prototype of the Google search engine, published in 1998. Héctor García-Molina and Jeff Ullman were also cited as contributors to the project.[32] PageRank was influenced by a similar page-ranking and site-scoring algorithm earlier used for RankDex, developed by Robin Li in 1996, with Larry Page's PageRank patent including a citation to Li's earlier RankDex patent; Li later went on to create the Chinese search engine Baidu.[33][34]

# gle raised around $1,000,000, which is what allowed them to open up their original shop in Menlo Park, California.[46] Craig Silverstein, a fellow PhD student at Stanford, was hired as the first employee.[22][47][48]
# After some additional, small investments through the end of 1998 to early 1999,[43] a new $25 million round of funding was announced on June 7, 1999,[49] with major investors including the venture capital firms Kleiner Perkins and Sequoia Capital.[40] Both firms were initially reticent about investing jointly in Google, as each wanted to retain a larger percentage of control over the company to themselves. Larry and Sergey however insisted in taking investments from both. Both venture companies finally agreed to investing jointly $12.5 million each due to their belief in Google's great potential and through the mediation of earlier angel investors Ron Conway and Ram Shriram who had contacts in the venture companies.[50]"""
def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    # print(stopword)

    nlp=spacy.load('en_core_web_sm')
    # copying text in doc variable
    doc=nlp(rawdocs)  
    # print(doc)
    tokens=[token.text for token in doc]
    # print(tokens)
    # making a dictonary for count how many words is repeated in the given text eg{google:10,have:2} it means google having 10 times in text
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1    
    # print(word_freq)

    # tofingding max frequency in dictonary
    max_feq=max(word_freq.values())
    # print(max_feq)

    # we normilize the frequency 
    for word in word_freq.keys():
        word_freq[word]= word_freq[word]/max_feq
    # print(word_freq)    

    sent_tokens=[sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores= {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]    
    # print(sent_scores)

    select_len=int(len(sent_tokens)*0.3)
    # print(select_len)

    summary= nlargest(select_len,sent_scores, key=sent_scores.get)
    # print(summary)

    final_summary=[word.text for word in summary]
    summary =' '.join(final_summary)
    # print(text)
    # print('after summary')
    # print(summary)

    # print("length of origianl Text ",len(text.split(' ')))
    # print("length of summary Text is",len(summary.split(' ')))
    return summary,doc, len(rawdocs.split(' ')), len(summary.split(' ')) 


