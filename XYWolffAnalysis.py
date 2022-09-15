import matplotlib.pyplot as plt
from numpy import sqrt
from cmath import cos, sin
import matplotlib.pyplot as plt
from matplotlib import animation

targetFile = '/Users/Smith/Desktop/UnderGradProject/MINE/Smith_XY_Analysis_&_Visualization.txt'

thermCut = 5000  ##This tells the program what sweep to start calculating average values and stuff

with open(targetFile) as in_file:
    lines = in_file.readlines()
    visCheck = int(lines[0])    
    ##del lines[0]


if visCheck == 0:    ##BEGIN analysis section
    updates = 0
    dataE = []
    dataM = []
    dataAvgE = []
    dataAvgE2 = []
    dataAvgM = []
    dataAvgM2 = []
    count = 0
    ##expE = 0 
    ##expM = 0 
    ##200 should be plenty of updates for the system to thermalize

    with open(targetFile) as in_file:
        lines = in_file.readlines()
        line = lines[1].split(",", -1)
        size = int(line[0])
        updates = int(line[1])
        count = (len(line) - 2) ##This gets the number of different temperatures
        print("Size: ", size, " Updates: ", updates, " Temps: ") ##This just takes the first line from the text file and pulls out the size, number of updates, and the temperatures the updates were performed at

        print('Count: ',count)
        print('line[2]: ',line[2], ', line[3]: ', line[3], ', line[4]: ', line[4])
        name = ["" for k in range(count)]
        for x in range(count):
            name[x] = "J = " + str(line[x+2])
        if(updates <= thermCut):
            print("The number of updates is less than the thermCut! No analysis can be performed.")

        #print("count: ",count)
        dataEA = [[0 for x in range(updates+1)] for y in range(count+1)] ##Array that stores the energy density after each sweep, along with the "temperature" the sweep was performed at
        


        dataMA = [[0 for x in range(updates+1)] for y in range(count+1)] ##Array that stores the magnetizations of each sweep, along with the "temp"
        expE = [0 for y in range(count)]  ##This array stores the expectation value of the energy 
        expM = [0 for y in range(count)]  ##This array stores the expectation value of the magnetzation
        expE2 = [0 for y in range(count)]  ##This array stores the expectation value of the energy^2 
        expM2 = [0 for y in range(count)]  ##This array stores the expectation value of the magnetzation^2 
        errE = [0 for y in range(count)] ##This is the error for the estimate of <E>
        stdE = [0 for y in range(count)] ##This is the standard deviation for the estimate of <E>
        errM = [0 for y in range(count)] ##This is the error for the estimate of <M>
        stdM = [0 for y in range(count)] ##This is the standard deviation for the estimate of <M>
        sweepArr = [x for x in range(1,updates+1)] ##Just an array to serve as the x component of the data
        tempArr = [0 for x in range(count)] ##This array stores the temperatures the sims were performed at, and serves as x component of data

        print('right before delete: ', lines[0])
        del lines[0] ##Delete the first line in the text file, leaving just the data
        del lines[0]
        print('right after delete: ', lines[0])
        i = 0
        j = 1
        k = 1
        temp = ""
        check = False
        while i < count:
            temp = lines[updates*i].split(",",3)
            while j <= updates:
                if i == count - 1 and j == updates:
                    ##print("temp: ", temp[0])
                    pass

                line = lines[updates * i + (j-1)].split(",",7)
                ##print(line)
                dataEA[i][j] = (float(line[2]) / size)
                dataMA[i][j] = (float(line[3]))

                ##print("dataEA[",i,"][",j,"]: ",dataEA[i][j])
                
                ##print("lol")
                j+=1
            ##print("i: ",i)
            dataEA[i][0] = float(temp[0])
            dataMA[i][0] = float(temp[0])
            

            tempArr[i] = float(temp[0])



            j = 1
            i+=1

        i = 0
        while i < count: ##This loop is for calculating the expected values and their errors
            j = thermCut
            while j <= updates:
                expE[i] = expE[i] + dataEA[i][j] # <E>
                expE2[i] = expE2[i] + dataEA[i][j]*dataEA[i][j] # <E^2>
                expM[i] = expM[i] + dataMA[i][j] # <M> 
                expM2[i] = expM[i] + dataMA[i][j]*dataMA[i][j] # <M^2>
                j+=1

            expE[i] = expE[i] / (updates - thermCut - 1)   ##This makes expE[i][1] = <E> at a given temp (expE[i][0] stores the temp). This is an unbiased estimate, since we are ignoring the first ~200 updates, then adding the energies of the updates, then dividing by the number of updates - 200 - 1. If we didn't include that minus one, it would be a biased estimate I think
            expM[i] = expM[i] / (updates - thermCut - 1)   ##This is <M>, but everything else is the same as expE
            expE2[i] = expE2[i] / (updates - thermCut - 1) ##This is the expectation value of the energy^2 or <E^2>
            expM2[i] = expM2[i] / (updates - thermCut - 1) ##This is <M^2>
            ##print('expE2[',i,']: ', expE2[i], ', expE[',i,']*expE[',i,']: ', expE[i]*expE[i])
            stdE[i] = sqrt(abs(expE2[i] - (expE[i]*expE[i]))) ##I think theres supposed to be an abs() in here, but I'm not sure
            stdM[i] = sqrt(abs(expM2[i] - (expM[i]*expM[i])))
            errE[i] = stdE[i] / sqrt((updates - thermCut - 1))  ##I'm not sure if were supposed to subtract one like we did for the expectation value, but I'll leave it for now
            errM[i] = stdM[i] / sqrt((updates - thermCut - 1))
            i+=1
        i = 0
        
        ##print("dataEA[1]: ",dataEA[1])
        ##print("dataEA[18][500]: ",dataEA[18][500])
        fig = plt.figure(figsize = (10,8))
        eGraf = fig.add_subplot(221)
        plt.ylabel('Energy Density')
        plt.xlabel('Update')
        eAx = fig.add_subplot(223)
        plt.xlabel('Temp Modeled ( J )')
        plt.ylabel('<E>')
        mGraf = fig.add_subplot(222)
        plt.ylabel('Magnetization')
        plt.xlabel('Update')
        mAx = fig.add_subplot(224)
        plt.xlabel('Temp Modeled ( J )')
        plt.ylabel('<M>')
        
        for i in range(count):
            del dataEA[i][0]
            del dataMA[i][0] 
            eGraf.plot(sweepArr, dataEA[i], label = name[i])
            mGraf.plot(sweepArr, dataMA[i], label = name[i])
            #eGraf.plot(sweepArr[thermCut:], dataEA[i][thermCut:], label = name[i])
            #mGraf.plot(sweepArr[thermCut:], dataMA[i][thermCut:], label = name[i])
        i = 0
        

        #eGraf.legend(ncol = 1, loc = "center left", fontsize = 'small', borderaxespad = -4.0)
        mGraf.legend(loc = 'center', bbox_to_anchor=(.5, .906), bbox_transform = fig.transFigure, ncol = len(tempArr))
        fig.suptitle('Energy Density & Magnetization for Varying J (Using Wolff Cluster Algorithm)') ##Fix This
        eAx.scatter(tempArr, expE)
        eAx.errorbar(tempArr, expE, yerr= errE, fmt='o--')
        #eAx.ylabel('<E>')
        mAx.scatter(tempArr, expM)
        mAx.errorbar(tempArr, expM, yerr= errM, fmt='o--')
        #mAx.xlabel('Temp J')
        #mAx.ylabel('<M>')

        for x,y in zip(tempArr,expE):

            labelE = f"σ = {round(errE[i],5)}"
            eAx.annotate(labelE, (x,y), textcoords="offset points", xytext=(0,12), ha='center')
            i+=1
        i=0
        for x,y in zip(tempArr,expM):

            labelM = f"σ = {round(errM[i],5)}"
            mAx.annotate(labelM, (x,y), textcoords="offset points", xytext=(0,12), ha='center')
            i+=1
        i=0
        plt.figtext(.5,0.02, 'Note: The expectation values were calculated ignoring the first ' + str(thermCut) + ' updates', transform = fig.transFigure, horizontalalignment = 'center')
        plt.figtext(.5,0.94,"Lattice Size: " + str(int(sqrt(size))) + 'x' + str(int(sqrt(size))) + "   Updates: " + str(updates), transform = fig.transFigure, ha = 'center')

        plt.show()

elif (visCheck == 1):    ##BEGIN visualization section
    spins = []
    xComp = []
    yComp = []
    xPos = []
    yPos = []

    fig, ax = plt.subplots(figsize = (10,9))
    frames = []


    count = 0

    with open(targetFile) as in_file:
        lines = in_file.readlines()
        line = lines[1].split(",", -1)
        l = int(line[0])
        size = l*l
        updates = int(line[1])
        j = float(line[2])

        print('Size: ', l, 'x',l, ', Updates(frames): ', updates, ', J = ', j)

        spins = [0 for x in range(size)]
        xComp = [0 for x in range(size)]
        yComp = [0 for x in range(size)]
        xPos = [0 for x in range(size)]
        yPos = [0 for x in range(size)]
        color = [0 for x in range(size)]

        del lines[0]
        del lines[0]

        u = 0
        i = 0
        while u < updates:
            while i < size:
                line = lines[u*size + i].split(",",5)
                spins[i] = float(line[2])
                xPos[i] = int(line[3])
                yPos[i] = (int(line[4]) + l - 1)
                color[i] = int(line[5])
                xComp[i] = cos(spins[i])
                yComp[i] = sin(spins[i])
            
                ##print('spins[', i , ']: ', spins[i], ', xPos[', i, ']: ', xPos[i], ', yPos[', i, ']: ', yPos[i])
                i+=1
            
            
            pic = ax.quiver(xPos, yPos, xComp, yComp, color, pivot = 'mid', headwidth = 1.4, scale = 40, cmap='winter')
            picTitle = ax.text(0.5,1.05,"Update: {}".format(u+1), size=plt.rcParams["axes.titlesize"], ha="center", transform=ax.transAxes, )
            frames.append([pic, picTitle])
            i = 0
            u+=1
        
        ani = animation.ArtistAnimation(fig, frames, interval=3000, blit=False)
        plt.show()

