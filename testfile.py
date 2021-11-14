for i in xrange(0,10):
    print i

try:
    with open("abc") as f:
        f.read()
except FileNotFoundError, err:
    print "%s" % err

try:
    with open("abc") as f:
        f.read()
except FileNotFoundError , err:
    print "%s" % err

x = 0
print '{}'.format(x)

