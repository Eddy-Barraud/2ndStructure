#https://www.mdtraj.org/1.9.5/api/generated/mdtraj.compute_dssp.html#mdtraj.compute_dssp
# pyinstaller --onefile -w ".\DsspAny.py"
import mdtraj as md
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os, re

def doDssp(filename) :
    traj = md.load(filename+".xtc",top=filename+".gro")
    topology=traj.topology

    dssp=md.compute_dssp(traj, simplified=True)

    LidDsspMap={}
    tick=0
    for line in dssp :
        translatedDssp=[]
        for res in line:
            if res == 'C':
                translatedDssp.append(1)
            elif res == 'H' :
                translatedDssp.append(2)
            elif res == 'E' :
                translatedDssp.append(3)
            else:
                translatedDssp.append(0)
        LidDsspMap[int(traj._time[tick])]=translatedDssp
        tick+=1
    
    df=pd.DataFrame(data=LidDsspMap, index=None)

    resIndex=[]
    for i in range(0,topology._numResidues):
        resIndex+=re.findall("[0-9]+",str(topology.residue(i)))
    df.index = resIndex

    dfT=df.transpose()

    customCmap = LinearSegmentedColormap.from_list(
        name='custom',
        colors=['white','green','red']
    )

    plt.rcParams['figure.figsize'] = [8.0, 8.0]
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['savefig.dpi'] = 400

    fig, ax = plt.subplots()
    ax = sns.heatmap(dfT, vmin=1, vmax=3,cmap=customCmap, ax=ax)
    ax.invert_yaxis()
    ax.set_ylabel("Time (ps)")
    ax.set_xlabel("Residue N°")
    plt.savefig(filename+'.dssp.png')

    # Uncomment everything below and change the range(#,#) if wanted
    #dfT2=df.loc[[str(i) for i in range(40,57)]].transpose()
    #fig, ax = plt.subplots()
    #ax = sns.heatmap(dfT2, vmin=1, vmax=3,cmap=customCmap, ax=ax)
    #ax.invert_yaxis()
    #ax.set_ylabel("Time (ps)")
    #ax.set_xlabel("Residue N°")
    #plt.savefig(filename+'.dssp.LID.png')

    print("1: Coil or Undefined; 2: Helix; 3: Strand")
    return True


for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if(file.endswith(".xtc") and not os.path.exists(os.path.splitext(file)[0]+".dssp.png")):
            #print(os.path.join(root,file))
            doDssp(os.path.splitext(file)[0])
