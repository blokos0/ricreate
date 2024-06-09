import glob
import cv2

dictnames = glob.glob("dict/*.png")
dict = [cv2.imread(file) for file in dictnames] # load the dictionary

img = cv2.imread("img.png") # load the image

rows, cols, _ = img.shape

img_split = []
for r in range(0, rows, 24):
    for c in range(0, cols, 24):
        img_split.append(img[r : r + 24, c : c + 24, :]) # split the image into 24x24 segments

str = "" # define the string and flags

curimgspl = 0 # current image split
for i in range(rows // 24):
    for j in range(cols // 24):
        tile = "error"
        diff = 9999999
        ind = 0 # tile name index
        indcur = 0
        for d in dict:
            # diffcur = sum(sum(sum(cv2.subtract(img_split[curimgspl], d))))
            diffcur = sum(sum(cv2.absdiff(cv2.mean(d), cv2.mean(img_split[curimgspl])))) # i have no idea what im doing
            if diffcur < diff:
                ind = indcur
                diff = diffcur
            print(f"s{curimgspl}, bd{diff}, bt{dictnames[ind]}, cd{diffcur}, ct{dictnames[indcur]}")
            indcur += 1
            if diff == 0:
                break
        print(f"{dictnames[ind]} for s{curimgspl}")
        tile = dictnames[ind][5 : len(dictnames[ind]) - 4]
        str += f"{tile}"
        if j != cols // 24 - 1:
            str += " "
        curimgspl += 1
    str += "\n"
with open("out.txt", "w") as f:
    print(str, file = f)
print("done! output is in out.txt")