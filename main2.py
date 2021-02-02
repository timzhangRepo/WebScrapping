import json
import csv

f = open("Google_Result1.json");
googleRs = json.load(f);
f = open("bing.json");
bingRs = json.load(f);

linksShared = []
def compareRs(googleR, otherR):
    Set = set()
    shared = []
    for link in googleR:
        if(link[-1]=='/' or link[-1]==' '):
            link = link[:-1]
        Set.add(link.split("://")[1])
    for link in otherR:
        link = link.split("://")[1]
        if(link[-1]=='/' or link[-1]==' '):
            link = link[:-1]
        if link in Set:
            shared.append(link)
            Set.remove(link)
    linksShared.append(shared)
    return len(Set)
count = 0;
def spearman(googleR, otherR, numQuery):
    linkShared = linksShared[numQuery-1]
    if(len(linkShared)==0): return 0
    if(len(linkShared)==1):
        idx = 0
        for gl in googleR:
            if(linkShared[0] in gl):
                if(linkShared[0] in otherR[idx]): return 1;
            idx+=1
        return 0;
    gRank = 0;
    oRank = 0;
    diSqr = 0;
    for link in linkShared:
        for gl in googleR:
            gRank+=1;
            if (link in gl): break;
        for ol in otherR:
            oRank+=1;
            if (link in ol): break;
        diff = gRank-oRank
        gRank = 0 #Reset
        oRank = 0 #Reset
        diSqr += diff*diff
    fenzi = diSqr*6
    fenmu = len(linkShared)*(len(linkShared)*len(linkShared)-1)
    return 1-(fenzi/fenmu)
print("Queries," + " Number of Overlapping Results," + " Percent Overlap," + " Spearman Coefficient")
av_overlap = 0
av_percentLap = 0
av_Spearman = 0

with open('restuls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key in googleRs:
        googleR = googleRs[key]
        bingD = bingRs[count]
        bingR = bingD[key + " "]
        count += 1
        Overlap = 10 - (compareRs(googleR, bingR))
        av_overlap += Overlap
        OverLapPercent = Overlap / 10;
        av_percentLap += OverLapPercent
        spearmanValue = spearman(googleR, bingR, count)
        av_Spearman += spearmanValue
        print("Query" + str(count) + ", " + str(Overlap) + ", " + str(OverLapPercent * 100) + ", " + str(
            round(spearmanValue, 2)))
        writer.writerow(["Query " + str(count), str(Overlap), str(OverLapPercent * 100), str(
            round(spearmanValue, 2))])
av_overlap = av_overlap/100
av_percentLap = av_percentLap/100
av_Spearman = av_Spearman/100


print(av_overlap, av_percentLap, av_Spearman)
