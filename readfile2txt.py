import os

def readfiles(imagepath, maskpath,txtfile):
	files = os.listdir(imagepath)
	f = open(txtfile, "w")
	for file in files:
		print("[INFO] writing {}".format(file))
		text = os.path.join(imagepath, file) + " " + os.path.join(maskpath, file) + "\n"
		f.write(text)
	f.close()

if __name__ == "__main__":
	imagepath = "/media/dp/LinuxData/DataSets/temp/out/JPEGImages"
	maskpath = "/media/dp/LinuxData/DataSets/temp/out/Annotations"
	readfiles(imagepath, maskpath, 'test.txt')