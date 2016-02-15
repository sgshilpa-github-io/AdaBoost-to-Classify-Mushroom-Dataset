__author__ = 'shilpagulati'

import sys
import math



def EntropyGain(ClassColumn,FeatureColumn,Featurecandidates,weights):

    Features= list(set(FeatureColumn))
    Attributecandidates=[]

    for each in Features:
        counte=0.0
        countp=0.0

        for i in range(0,len(FeatureColumn)):
            if FeatureColumn[i]==each:
                if ClassColumn[i]=='e':
                    counte+=weights[i]
                elif ClassColumn[i]=='p':
                    countp += weights[i]
                else:
                    print "wrong class name"
        Attributecandidates.append([each,[countp,counte]])


    return Gain(Attributecandidates,Featurecandidates)


#return the entropy of each Attribute of feature

def CalculateEntropy(EachAttribute):


    total_weight=EachAttribute[0]+EachAttribute[1]

    value=0.0
    total_weight=EachAttribute[0]+EachAttribute[1]
    for each in EachAttribute:


        if each!=0:
            value-=(each/total_weight)*(math.log((each/total_weight),2))

    return value

   # returns the gan of attribute

def Gain(Attributecandidate,Featurecandidate):

    totalWeight=Featurecandidate[0][0]+Featurecandidate[0][1]
    Gain_F=CalculateEntropy(Featurecandidate[0])
    # print "Paren Entrop"+str(Gain_F)




    for each in Attributecandidate:
        # print "each"+str(each)
        # print "Entropy "+str(CalculateEntropy(each[1]))



        Gain_F-=((each[1][0]+each[1][1])/totalWeight)*(CalculateEntropy(each[1]))


    return Gain_F









#return the selected feature

def FeatureSelection(MainValues,weights):
    counte = 0.0
    countp=0.0
    Featurecandidates=[]
    for i in range (0,len( MainValues[0])):
        if MainValues[0][i]=='e':
            counte+=weights[i]
        elif MainValues[0][i]=='p':
            countp+=weights[i]
        else:
            print "error in input"
    Featurecandidates.append([countp,counte])


    AllGain=[]
    for i in range(1,len(MainValues)):

        AllGain.append(EntropyGain(MainValues[0],MainValues[i],Featurecandidates,weights))
    # print AllGain

    Classifier.setdefault("Feature Index",AllGain.index(max(AllGain))+1)

    return adaboost(MainValues,Classification(MainValues, MainValues[AllGain.index(max(AllGain))+1],weights),weights)


#
def Classification(MainValues,FeatureColumn,weights):



    Features= list(set(FeatureColumn))
    EdibleList=[]
    PoisonousList=[]
    TempClassification=[]
    for attribute in Features:
        counte=0.0
        countp=0.0
        for i in range(0,len(FeatureColumn)):
            if FeatureColumn[i]==attribute:
                if MainValues[0][i]=='p':
                    countp+=weights[i]
                elif MainValues[0][i]=='e':
                    counte+=weights[i]
                else:
                    print "wrong input values"

        if counte>=countp:
            Classifier.setdefault(attribute,'e')
            EdibleList.append(attribute)

        else :
            Classifier.setdefault(attribute,'p')
            PoisonousList.append(attribute)

    for i in range(0,len(FeatureColumn)):
            if FeatureColumn[i]in EdibleList:
                TempClassification.insert(i,'e')
            elif FeatureColumn[i] in PoisonousList:
                TempClassification.insert(i,'p')

    return TempClassification



def adaboost(Mainvalues,TempClassification,weights):
    esp=0.0

    for i in range(0,len(Mainvalues[0])):
        if Mainvalues[0][i]!=TempClassification[i]:
            esp+=weights[i]
    # print esp
    EspValues.append(esp)
    alpha=0.5*math.log(((1-esp)/esp),math.e)
    AlphaValues.append(alpha)
    Classifier.setdefault('alpha',alpha)




    # count=0
    # for i in range(0,len(Mainvalues[0])):
    #
    #     if TempClassification[i]!=Mainvalues[0][i]:
    #         print i
    #         count+=1
    # print count

    #calculate Z

    Z=0.0
    for i in range(0,len(weights)):
        if Mainvalues[0][i]!=TempClassification[i]:
            Z+=weights[i]*math.exp(alpha)
        else:
            Z+=weights[i]*math.exp(-alpha)
    # print Z
    for i in range(0,len(weights)):
       if Mainvalues[0][i]!=TempClassification[i]:
           weights[i]=(weights[i]*math.exp(alpha))/Z
       else:
           weights[i]=(weights[i]*math.exp(-alpha))/Z

    Hypothesis.append(Classifier)
    return weights

Hypothesis=[]

AlphaValues=[]
EspValues=[]
def main():

    Iterations=int(sys.argv[1])
    input=open(sys.argv[2]).read().split('\r')

# stores file in rowise

    AllValues=[]
    for each in input:
        AllValues.append(each.split('\t'))

# stores all the values in column format

    MainValues=[]
    for i in range(0,len(AllValues[0])):
        TempValues=[]
        for each in AllValues:
            TempValues.append(each[i])

        MainValues.append(TempValues)


# Assign initial weight =1/no of test rows

    weights=[]
    for i in range(0,len(MainValues[0])):
        weights.append(float(1)/len(MainValues[0]))


    i=1
    while(i<=Iterations):
        global Classifier
        Classifier={}
        weights= FeatureSelection(MainValues,weights)
        i+=1
    # print Hypothesis
    testing()


def testing():
    testinput=open(sys.argv[3]).read().split('\r')

    AllTesting=[]
    for each in testinput:
        AllTesting.append(each.split('\t'))


    Predicted_Label=[]
    for line in AllTesting:
        predictedValue=0.0
        for i in range(0,len(Hypothesis)):
            if line[Hypothesis[i]['Feature Index']] in Hypothesis[i]:
                if Hypothesis[i][line[Hypothesis[i]['Feature Index']]]=='p':
                    predictedValue+=Hypothesis[i]['alpha']
                if Hypothesis[i][line[Hypothesis[i]['Feature Index']]]=='e':
                    predictedValue-=Hypothesis[i]['alpha']
            else:
                predictedValue+=Hypothesis[i]['alpha']
        if predictedValue>0:
            Predicted_Label.append('p')
        else:
             Predicted_Label.append('e')


    count=0.0

    for i in range(0,len(AllTesting)):

        if AllTesting[i][0]!=Predicted_Label[i]:
            count+=1

    Accuracy= (len(AllTesting)-count)/len(AllTesting)
    print Accuracy*100
    for each in AlphaValues:
        print each



if __name__=='__main__':
    main()
