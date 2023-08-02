list1 = ["cool", "trees", "awesome", "wow"]

for index, item in enumerate(list1):
    if index > 1:
        del list1[index:len(list1)]
print(list1)