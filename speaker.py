# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:19:40 2022

@author: erick
"""

import speech_recognition as sr
from termcolor import colored
from config import config
import difflib
import statistics
import pandas as pd

class Speaker(object):
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.path_text = config.PATH_TEXT
        
        self.text = []
        self.translate = []
        
    def read_file(self):
        df = pd.read_excel(self.path_text)
        
        self.text = df['text'].tolist()
        self.translate = df['translate'].tolist()
        
    def speak(self):
        microphone = sr.Recognizer()
        with sr.Microphone() as src:
            microphone.adjust_for_ambient_noise(src)
            print('Sua vez!')
            voice = microphone.listen(src)
            
        try:
            phrase = microphone.recognize_google(voice, language="de-DE")
            #print(f'Você disse: {phrase}')
        except sr.UnkownValueError:
             print("Erro desconhecido")
             
        return phrase

    def correct(self,s1, s2):
        matcher = difflib.SequenceMatcher(a=s1, b=s2)
        
        correct = []
        for match in matcher.get_matching_blocks():
            correct.append((match[0], match[0] + match[2]))
            
        for i in range(len(s1)):
            
            right = False
            for c in correct:
                if c[0] <= i <= c[1]:
                    right = True
                    break
        
            
            if right:
                print(colored(s1[i], 'green'), end='')
            else:
                print(colored(s1[i], 'red'), end='')
                
        accuracy = round(matcher.ratio() * 100, 2)
            
        return accuracy
    
    def play(self):
        input('Vamos começar?\n')
        score = []
        for text, translate in zip(self.text, self.translate):
            while True:
                print(f'Leia: {text}')
                phrase = self.speak()
                print('Você leu: ', end='')
                
                phrase_to_correct = phrase.lower().strip()
                text_to_correct = text.lower().strip().replace(',','')
                accuracy = self.correct(text_to_correct,phrase_to_correct)
                print("")
                print(f'Tradução: {translate}')
                print(f'Acurácia: {accuracy}%')
                
                x = input('Tentar Novamente? [s] para Sim, [n] para Não: ')
                print("")
                if x != 's':
                    score.append(accuracy)
                    break
            
        mean_score = statistics.mean(score)
        print(f'Parabéns! Pontuação final: {round(mean_score,2)}%')
    
    def run(self):
        self.read_file()
        self.play()