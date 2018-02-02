#!/usr/bin/env python3
import os
import sys
import wget
import getopt
import zrif2rif as z2r
from shutil import copy2

package = None
zrif = None

opts, rest = getopt.getopt(sys.argv[1:], "p:z:")
for opt, arg in opts:
	if opt == '-p':
		package = arg
	if opt == '-z':
		zrif = arg
if package == None:
	print("pdb_creator v.1.0.0")
	print("")
	print("Usage:")
	print("	  pdb_creator [-p filename.pkg] [-z ZRIF]")
	print("")
	print("Parameters:")
	print("	  -p			Input Theme PKG")
	print("	  -z			Zrif")
	print("")
	sys.exit("Error: No Input Package specified !")
if zrif == None:
	print("pdb_creator v.1.0.0")
	print("")
	print("Usage:")
	print("	  pdb_creator [-p filename.pkg] [-z ZRIF]")
	print("")
	print("Parameters:")
	print("	  -p			Input Theme PKG")
	print("	  -z			ZRif")
	print("")
	sys.exit("Error: No ZRif-String specified !")

def exists(path):
    """
    Test whether a path exists.
    Returns False if not found.
    """
    try:
        status = os.stat(path)
    except os.error:
        return False
    return True

folder_number = int(1)

while exists("bgdl/t/{}".format("0000000" + str(folder_number))) == True:
	folder_number += 1

while len(str(folder_number)) != len("00000001"):
	folder_number = "0" + str(folder_number)

while len(folder_number) > len("00000001"):
	folder_number = folder_number[1:]

cid = z2r.cid_fetch(package)
tid = z2r.offsets_read(package, 55, 63)

z2r.zrif2rif(zrif, "bgdl/t/{}/{}/sce_sys/package/work.bin".format(folder_number, tid.decode("utf-8")))
z2r.syscmd('pkg_dec {} bgdl/t/{}/{}/'.format(package, folder_number, tid.decode("utf-8")))

if len(tid) != len("PCSG90218"):
	tid = tid + b'\x00'


# Copy Files:
copy2("assets/icon.png", "bgdl/t/{}/icon.png".format(folder_number))
copy2("assets/d0.pdb", "bgdl/t/{}/d0.pdb".format(folder_number))
copy2("assets/d1.pdb", "bgdl/t/{}/d1.pdb".format(folder_number))
copy2("assets/f0.pdb", "bgdl/t/{}/f0.pdb".format(folder_number))

# Write to Files:

z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 634, cid.encode("utf-8")) # CID
z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 778, tid) # TITLE_ID
z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 852, tid) # TITLE_ID_2


z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 634, cid.encode("utf-8")) # CID
z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 778, tid) # TITLE_ID
z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 852, tid) # TITLE_ID_2
