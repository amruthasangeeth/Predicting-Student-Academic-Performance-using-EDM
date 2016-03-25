from __future__ import division
from numpy import *
from math import log

import operator
import pandas as pd
import collections

def countItemsInColData(columnData):
        return collections.Counter(columnData);

def InfoGainClass(data,Classifier):
        index = data.columns.get_loc(Classifier);
        columnData = data.ix[:,index];
        N=len(columnData);
        items = columnData.unique();
        itemCount = countItemsInColData(columnData);

        #print items,N;
        answer = 0;
        
        for i in items:
                pi = (itemCount[i]/N);
                answer = answer + (-1)*pi*log(pi);
        return answer/log(2);        

def InfoGain(data,columnName,Classifier): 
        index = data.columns.get_loc(columnName);
        columnData = data.ix[:,index];
        index2 = data.columns.get_loc(Classifier);
        ClassifierData = data.ix[:,index2];
        
        items = columnData.unique();
        classes = ClassifierData.unique();
        itemCount = countItemsInColData(columnData);
        
        InfoGainOfItems = {};
        zero_i = items[0];
        zero_j = classes[0];
        
        
        
        for i in items :
                gain = 0;
                N = itemCount[i];
                for j in classes:
                        #print i,'and',j;
                        intersection = len(data[(data.ix[:,index] == i) & (data.ix[:,index2] == j)])
                       # print intersection, 'and', N;
                        pi = intersection/N;
                        
                        if(pi==1):
                        #        print 'SUCCESS',i,j;
                                zero_i=i;
                                zero_j=j;
                                
                        if(pi!=0):
                                gain = gain + (-1)*pi*log(pi)/log(2);
                InfoGainOfItems[i]=gain; 

       
        TotalRows = 0;
        for i in itemCount:
                TotalRows = TotalRows + itemCount[i];
        
        answer  = 0;
        #print InfoGainOfItems;
        for i in items:
                 answer = answer + (itemCount[i]*InfoGainOfItems[i]/TotalRows);

        return answer,zero_i,zero_j;
       

def create_tree(data,Classifier):      
#                print data;
                ClassifierIndex = data.columns.get_loc(Classifier);
                attributes = list(data.columns.values); 
                attributes.remove(Classifier);
                ClassifierInfoGain = InfoGainClass(data,Classifier);
                max_value = 0;
                
                node = attributes[0];
                gain,path,clas =  InfoGain(data,node,Classifier); 
                
                for i in attributes:
                        if(i != Classifier): 
                                gain,local_path,local_clas =  InfoGain(data,i,Classifier); 
                                
                                if(max_value < (ClassifierInfoGain - gain)):
                                        max_value = ClassifierInfoGain - gain;
                                        node = i;
                                        path = local_path;
                                        clas = local_clas;
                                        
                #print max_value; 
                
                print "\n",node,'>>>>>> Transition [',path,'] >>>>>>',clas;
                data = data[(data.ix[:,node] != path)]; 

                for i in  data.ix[:,node].unique():
                                        print "Current Parent Node :",node;
                                        print ">>>>>> Transition[",i,"]";
                                        NewData = data[data.ix[:,node]==i];
                                        NewData.drop(node,inplace=False,axis=1)
                                        create_tree(NewData,Classifier);
                                        print "Returns back to parent : >>" ,node

if __name__ == "__main__":
 CSVData = pd.read_csv('data.csv')
 create_tree(CSVData,'Rclass')
 
