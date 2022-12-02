import traceback
try:
    file = open('signalDistance.txt', 'w')
    file.write("1")
    file.close()
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.close()
