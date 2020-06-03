"""
TEXT PREPROCESSING FOR BUILDING NMTS

@author: vasudevgupta
"""

import spacy
import re
import contractions
import unicodedata

import random
import pandas as pd
import os
os.chdir('/Users/vasudevgupta/Desktop/seq2seq/nmts_attention')

"""
FILE READING AND INPUT OUTPUT SEPEARTION
INPUT- ENGLISH
OUTPUT- GERMAN
"""
#with open('text/deu.txt', 'r') as file:
#    data= file.read()
#    dataset= data.split('\n')
#eng= []
#ger= []
#idx= random.sample(range(len(dataset)), params.num_samples)
#for i in idx:
#    e, g, _= dataset[i].split('\t')
#    eng.append(e.lower())
#    ger.append(g.lower())
#df= pd.DataFrame([eng, ger], index= ['eng', 'ger']).T

class preprocess_text:
    """
    DATA PREPROCESSING- NLP
        
        1) LOWERCASE ALL THE WORDS
        2) EXPAND CONTRACTIONS
        3) REMOVE ACCENTS
        4) PUT SPACE BW TOKENS
        5) <SOS>, <EOS> TOKENS APPEND
        6) MAKE VOCAB
        7) DO PADDING TO MAKE CONSTANT SEQ LENGTH IN A BUNDLE
    """
    
    def __init__(self):
        pass
    
    def remove_pattern(self, text, pattern= r'[^a-zA-Z0-9.!?, ]', replace_with= ""):
        return re.sub(pattern, replace_with, text)
    
    def tokenize_sent(self, text, nlp):
        doc= nlp(text)
        return [sent.text for sent in doc.sents]
    
    def tokenize_words(self, text, nlp):
        doc= nlp(text)
        return " ".join(tok.text for tok in doc)
    
    def expand_contractions(self, text):
        # import contractions
        # print(contractions.contractions_dict)
        return contractions.fix(text)
        
    def do_lemmatization(self, text, nlp):
        doc= nlp(text)
        return ' '.join(tok.lemma_ if tok.lemma_ != "-PRON-" else tok.text for tok in doc)
        
    def add_sos_eos(self, text, sos= False, eos= False):
        if (sos and eos):
            return "<sos> " + text + " <eos>" 
        if eos:
            return text + " <eos>"
        if sos:
            return "<sos> " + text
        return text
        
    def remove_accents(self, text):
        ## import unicodedata
        ## normalize text including accents --> ascii --> UTF-8
        # str(sents.numpy(), 'utf-8') == sents.numpy().decode('utf-8')
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('UTF-8', 'ignore')

def call_preprocessing(df_col, nlp_en= True, lower_= True, remove_pattern_= False, tokenize_words_= False,
               expand_contractions_= False, do_lemmatization_= False,
               sos= False, eos= False, remove_accents_= False):
    
    nlp= spacy.load('en_core_web_sm') if nlp_en else spacy.load('de_core_news_sm')
    prep= preprocess_text()
    
    if expand_contractions_:
        df_col= df_col.map(lambda text: prep.expand_contractions(text))
        
    if remove_accents_:
        df_col= df_col.map(lambda text: prep.remove_accents(text))
        
    if do_lemmatization_:
        df_col= df_col.map(lambda text: prep.do_lemmatization(text, nlp))
        
    if tokenize_words_:
        df_col= df_col.map(lambda text: prep.tokenize_words(text, nlp))
        
    if remove_pattern_:
        df_col= df_col.map(lambda text: prep.remove_pattern_(text))
    
    if eos or sos:
        df_col= df_col.map(lambda text: prep.add_sos_eos(text, sos, eos))
        
    # do lower if expanding contractions
    if lower_:
        df_col= df_col.map(lambda text: text.lower())
    return df_col

def tokenizer(df_col, nlp_en= True):
    vocab= set()
    _= [[vocab.update([tok]) for tok in text.split(" ")] for text in df_col]
    ## need to append "<sos> " token " <eos>" depending on what is df_col
    if not nlp_en:
        vocab.update(["<sos>"])
        vocab.update(["<eos>"])
    # 0 is reserved for padding
    tokenize= dict(zip(vocab, range(1, 1+len(vocab))))
    detokenize= dict(zip(range(len(vocab)), vocab))
    return tokenize, detokenize, len(vocab)

#df['eng_input']= call_preprocessing(df['eng'], nlp_en= True, lower_= True, remove_pattern_= False, tokenize_words_= True,
#                expand_contractions_= True, do_lemmatization_= False,
#                sos= False, eos= False, remove_accents_= True)
#
#df['ger_input']= call_preprocessing(df['ger'], nlp_en= False, remove_pattern_= False, tokenize_words_= True,
#                expand_contractions_= False, do_lemmatization_= False,
#                sos= True, eos= False, remove_accents_= True)
#
#df['ger_target']= call_preprocessing(df['ger'], nlp_en= False, remove_pattern_= False, tokenize_words_= True,
#                expand_contractions_= False, do_lemmatization_= False,
#                sos= False, eos= True, remove_accents_= True)

# df.to_csv('text/eng2ger.csv', index= False)
