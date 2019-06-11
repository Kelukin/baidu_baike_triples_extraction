import random

inputFile = "./baiduCard.txt"
upboundary  = 4003897
def baike_sample(num, outputFile = ""):
    assert(num>0 and num <= upboundary)
    if outputFile == "":
        outputFile = "./sampleResult_" + str(num) + ".txt"
    sampleLine = set()
    while(len(sampleLine)<num):
        sampleLine.add(random.randint(0,upboundary-1))
    sampleLine = sorted(sampleLine)

    with open(inputFile, "r") as input:
        output = open(outputFile,"w")
        no = 0
        sample_index = 0
        while(sample_index < num):
            line = input.readline()
            if no == sampleLine[sample_index]:
                output.write(line)
                sample_index += 1
            no += 1
        output.close()

if __name__ == "__main__":
    baike_sample(5000)
