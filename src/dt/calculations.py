import math

# Calculate the average for a set of values
def calculateAverage(values):
    return sum(values)/len(values)

# Calulate the variance for a set of values
def calculateVariance(values):
    average = calculateAverage(values)

    aux = 0
    for value in values:
        aux += (value - average)**2 # Difference to the power of 2

    return aux/len(values)

# Calculate the standard deviation for a set of values
def calculateDeviation(values):
    variance = calculateVariance(values)
    return math.sqrt(variance)

# Calculate the Simple Mobile Average
def calculateSMA(values, step):
    n = len(values)
    listSMA = []

    for i in range(step-1, n):
        sum = 0
        for j in range(0, step):
            sum += values[i-j]
        listSMA.append(sum/step)
    
    return listSMA


# Calculate the Exponential Mobile Average 
def calculateEMA(values):
    n = len(values) # Number of values
    listEMA = [0]*n
    k = 2 / (n + 1)
    
    # The first value has as EMA its own value
    listEMA[0] = values[0]
    
    for i in range(1, n):
        listEMA[i] = values[i]*k + listEMA[i - 1]*(1 - k)
    
    return listEMA