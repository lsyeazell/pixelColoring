import numpy
import random
from PIL import Image
import copy
import time

#still need to figure out best way to determine K
# pixels must be flatten or 1D
def K_Means(pixels, K):
    
    pix = numpy.array(pixels)
    
    outputs = []
    for i in range(3):
        centroids = random.sample(pixels,K)
        centroids = numpy.array(centroids)
        groups = {}
        for x in range(1,len(centroids)+1):
            groups[x] = []
        for ite in range(10):
            totalErr = 0
            toAverage = copy.deepcopy(groups)
            #assigns pixels to clusters
            for i in range(len(pixels)):
                minErr = numpy.power(numpy.dot(numpy.subtract(pixels[i],centroids[0]), (numpy.subtract(pixels[i],centroids[0])).T),2)
                minNum = 1
                for j in groups:
                    err = numpy.power(numpy.dot(numpy.subtract(pixels[i],centroids[j-1]), (numpy.subtract(pixels[i],centroids[j-1])).T),2)
                    if err<minErr:
                        minErr = err
                        minNum = j
                if ite ==9:
                    groups[minNum].append([i,pixels[i]])
                toAverage[minNum].append(numpy.array(pixels[i]))
                totalErr+=minErr
            toRemove = []
            for cluster in groups:
                c = numpy.array(toAverage[cluster])
                summ = numpy.sum(c,axis=0)
                length = len(toAverage[cluster])
                if length==0:
                    toRemove.append(cluster)
                    continue
                avg = numpy.divide(summ, length)
                centroids[cluster-1] = avg
            for clusR in toRemove:
                groups.pop(clusR)
        print(totalErr/len(pixels))
        outputs.append([totalErr, groups,centroids])
    minOut = 0
    minOutErr = outputs[0][0]
    for out in range(1,len(outputs)):
        if outputs[out][0]<minOutErr:
            minOut = out
            minOutErr = outputs[out][0]
    print(minOut)
    return outputs[minOut][1], outputs[minOut][2]

        
            
##for i= 1:size(X,1),
##	min = (X(i,:)-centroids(1,:))*(X(i,:)-centroids(1,:))';
##	minNum = 1;
##	for j = 2:K,
##		err = (X(i,:)-centroids(j,:))*(X(i,:)-centroids(j,:))';
##		if err<=min,
##			min = err;
##			minNum = j;
##		end
##	end
##	idx(i) = minNum;
##end







def flatten(pixels,size):
    x = size[0]
    y = size[1]
    flat = []
    for i in range(y):
        for j in range(x):
            flat.append(pixels[j,i])
        
    return flat


##
##im = Image.open("meTestImage.jpg")
##pixels  = im.load()
##size = im.size
##
##flat = flatten(pixels,size)
##time1 = time.perf_counter()
##groups, centroids = K_Means(flat,10)
##print(time.perf_counter()-time1)
##for cluster in groups:
##    print(tuple(centroids[cluster-1]))
##    for point in groups[cluster]:
##        pixels[point[0]%size[0],point[0]//size[0]] = tuple(centroids[cluster-1])
##
##im.show()



