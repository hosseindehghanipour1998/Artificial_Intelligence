import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from ExtraLibraries.Writer import Writer as Writer

class CommandCenter :
    TEST_SIZE = 0.2
    TRAIN_SIZE = 1 - TEST_SIZE
    BOUNDARY_PROBABILTY = 0.5
    PLOT_SCALER = 0.5


class DataCenter :
    X_train = None
    Y_train = None
    X_test  = None
    Y_test = None
    Thetas = None
    FILE_NAME = "iris.csv"
    X = None
    Y = None
    

def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def hypothesis(X, Thetas):
    z = np.dot(X, Thetas)
    d = sigmoid(z)
    return d


def costFunction(X, Y, Thetas):
    m = len(Y)
    h = hypothesis(X, Thetas)
    cost = Y * np.log(h) + (1 - Y) * np.log(1 - h)
    return cost.sum() / m


def updateThetas(X, Y, Thetas, alpha ):
    m = len(X)
    h = hypothesis(X, Thetas)
    gradient = (np.dot(X.T, h - Y) / m) * alpha
    Thetas = Thetas - gradient
    return Thetas



def train(X, Y, Thetas, alpha, iters):
    costLog = []

    for i in range(iters):
        Thetas = updateThetas(X, Y, Thetas, alpha)
        cost = costFunction(X, Y, Thetas)
        costLog.append(cost)

    return Thetas, costLog


def ReadData(fileName):
    dataSet = pd.read_csv(fileName)
    dataSet = dataSet[dataSet.Result != "Iris-versicolor"]
    #dataSet = dataSet[dataSet.Result != "Iris-virginica"]
    dataSet["Result"] = dataSet["Result"].apply(lambda x : 1 if x == "Iris-setosa" else 0 )
    
    # Create X (all the feature columns)
    X = dataSet.drop("Result", axis=1)
    DataCenter.X = X

    # Create y (the target column)
    Y = dataSet["Result"]
    DataCenter.Y = Y

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=CommandCenter.TEST_SIZE)
    
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    X_test = np.array(X_test)
    Y_test = np.array(Y_test)
    
    # Add Bias to our Features Matrix
    X_train = np.c_[np.ones((X_train.shape[0], 1)), X_train]
    X_test = np.c_[np.ones((X_test.shape[0], 1)), X_test]
    
    
    '''
     Here, our X is a two-dimensional array and y is a one-dimensional array. 
     Let’s make the ‘y’ two-dimensional to match the dimensions.
    '''
    Y_train = Y_train[:, np.newaxis]
    Y_test = Y_test[:, np.newaxis]
    
    
    return X_train , Y_train , X_test , Y_test


def calculate_accuracy():
    
    h = hypothesis(DataCenter.X_test,DataCenter.Thetas)
    def decisionBoundry(h):
        h1 = []
        for i in h:
            if ( i >= CommandCenter.BOUNDARY_PROBABILTY).any():
                h1.append(1)
            else:
                h1.append(0)
        return h1
    y_pred = decisionBoundry(h)
    accuracy = 0
    for i in range(0, len(y_pred)):
        if (y_pred[i] == DataCenter.Y_test[i]).any():
            accuracy += 1
    return (accuracy/len(DataCenter.Y_test)* 100) 


   
def showInfo(X_train,X_test, accuracy ,history):
    
    trainingSetLenght = len(X_train)/(len(X_train) + len(X_test)) * 100
    testSetLenght = len(X_test)/(len(X_train) + len(X_test)) * 100
    print("Training Set Length : %d Percent " %  trainingSetLenght)
    print("Test Set  Length : %d percent" % testSetLenght )
    print("Test Set  Accuracy : %d percent" %accuracy)
    for i in range(len(history)):
        if(i % 10000 == 0 ):
            print("Error : %f | ItNo : %d" %(history[i],i))

    #S = "Training Set Length :" + str(trainingSetLenght) + " Percent \n" + "Test Set  Length : "+ str(testSetLenght)+" Percent \n"  + "Test Set  Accuracy :"+str(accuracy)+" percent \n" 
    S = "TestSet : Accuracy :"+str(accuracy) + "%"
    print("============================")
    print("{0} + ({1})X1 + ({2})X2 = 0 " .format(DataCenter.Thetas[0],DataCenter.Thetas[1],DataCenter.Thetas[2]))
    print("Or in another words : ")
    print("X2 = [ X1 * ( {0} )  + ({1}) ]/({2})".format(DataCenter.Thetas[1],DataCenter.Thetas[0],DataCenter.Thetas[2]*(-1)) ) 
    print("============================")
    return S
        
def main() :
    print("Processing ... Please Wait.")
    DataCenter.X_train , DataCenter.Y_train , DataCenter.X_test , DataCenter.Y_test = ReadData(DataCenter.FILE_NAME) 
    initialThetas = np.zeros((3,1))
    DataCenter.Thetas, history = train(DataCenter.X_train, DataCenter.Y_train, initialThetas, 0.1, 100000)
    plotInf = showInfo(DataCenter.X_train,DataCenter.X_test, calculate_accuracy(),history )
    path  = Plotter.createNewDirectory("Plots/folderNumber.txt")
    Plotter.plotter("TrainSet" , DataCenter.X_train[:,1] , DataCenter.X_train[:,2] , DataCenter.Y_train ,path )
    Plotter.plotter(plotInf , DataCenter.X_test[:,1] , DataCenter.X_test[:,2] , DataCenter.Y_test ,path)
    

class Plotter :

    def saveFig(plotPointer , figName , figNumbPath ):
        filerIO = Writer(figNumbPath)
        lines = filerIO.readFile()
        if ( len(lines) == 0 ):
            filerIO.append(1) 
            lines[0] = 1 
        plotPointer.savefig( str(figName) + str(lines[0]) + '.png')
        filerIO.clearFile()
        filerIO.append(str(int(lines[0]) + 1) )   
        print("Figure saved in : " + str(figName))
      
    def plotter(plotInf, X0set , X1set , ResultSet , path ):
        scaler = CommandCenter.PLOT_SCALER
        X0 = ( X0set )
        weights = DataCenter.Thetas
        X1 = ( X1set )

        class_A = []
        class_B = []

        for i in range(len( ResultSet)) :
            if(ResultSet[i] == 0) :
                class_A.append(i)
            else :
                class_B.append(i)
        
        # getting the x co-ordinates of the decision boundary
        x_cords = np.array([min(X0) - scaler, max(X0) + scaler])
        y_cords = (weights[1] * x_cords + weights[0]) * (-1 / weights[2])
        # plot class A data with red color
        plt.scatter([X0[i] for i in class_A], [X1[i] for i in class_A], color='blue',  label='Iris-virginica')
        # plot class B data with red color
        plt.scatter([X0[i] for i in class_B], [X1[i] for i in class_B], color='red', label='Iris-setosa')
        
        # plot class B data with red color
        plt.plot(x_cords, y_cords, color = 'purple', label="Boundary")
        plt.legend()
        
 

        plt.xlabel('X0 - axis') 
        plt.ylabel('X1 - axis') 
        plt.title(" Logistic Regression : " + str(plotInf))  

        plt.legend()         
        Plotter.saveFig(plt , path + "/logistic" , "Plots/figureNumber.txt" )
        plt.show()

    def createNewDirectory(foldNumbPath):
        import os
        filerIO = Writer(foldNumbPath)
        lines = filerIO.readFile()
        if ( len(lines) == 0 ):
            filerIO.append(1)        
            lines[0] = 1
        os.mkdir( "Plots/Iteration-" +str(lines[0] ))   
        path = "Plots/Iteration-" + str(lines[0]) 
        filerIO.clearFile()
        filerIO.append(str(int(lines[0]) + 1) ) 
        return path
main()    
    
    
    
    
    
    
    
    
    
    
    
    