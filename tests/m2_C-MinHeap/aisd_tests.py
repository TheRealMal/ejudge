import sys
import os
import time
testTimes = {}

def test(file):
    sys.stdin = open('input/{}'.format(file), "r", encoding="utf8")
    sys.stdout = open('output/{}'.format(file), "w", encoding="utf8")
    import ejudjeTester
    startTime = time.time()
    ejudjeTester.main()
    endTime = time.time()
    testTimes[file] = (endTime-startTime)
    sys.stdin.close()
    sys.stdout.close()


inputs = next(os.walk(os.path.join('input')), (None, None, []))[2]

for file in inputs:
    test(file)


sys.stdout = open('output/{}'.format("timings.txt"), "w", encoding="utf8")
for _ in testTimes.keys():
    print("{} {}".format(_, testTimes[_]))
sys.stdout.close()

