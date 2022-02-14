import os
import sys
import shutil

def diff_kernel(org, patchfile, output):
    patched = open(patchfile, "rb").read()
    original = open(org, "rb").read()
    newfile = output
    test1 = open(patchfile, "rb").read(28)
    test2 = open(org, "rb").read(28)
    lenP = len(patched)
    lenO = len(original)
    if test1 != test2 or lenP != lenO:
        raw = open(org, "rb")
        fix = b"\xca\xfe\xba\xbe\x00\x00\x00\x01\x01\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x40\x00\x02\x31\x96\x78\x00\x00\x00\x0e"
        testPatched = open(f"{patchfile}.new", "w+b")

        testPatched.write(test2 + patched)

        testPatched.close()

        os.remove(patchfile)
        shutil.move(f"{patchfile}.new", patchfile)
        
    patched = open(patchfile, "rb").read()
    original = open(org, "rb").read()
    lenP = len(patched)
    lenO = len(original)
    if lenP != lenO:
        # CAFEBABE 00000001 0100000C 00000000 00004000 02319678 0000000E
        fix = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        testPatched = open(f"{patchfile}", "w+b")
        testPatched.seek(41020239)
        testPatched.write(fix)

        testPatched.close()

        
    diff = []
    for i in range(lenO):
        originalByte = original[i]
        patchedByte = patched[i]
        if originalByte != patchedByte:
            diff.append([hex(i),hex(originalByte), hex(patchedByte)])
    diffFile = open(newfile, 'w+')
    diffFile.write('#AMFI\n\n')
    for d in diff:
        data = str(d[0]) + " " + (str(d[1])) + " " + (str(d[2]))
        diffFile.write(data+ '\n')
