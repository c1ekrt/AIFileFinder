from filesys import Directory
from summary import Summary
# test_path = r"G:\Temp\3_研發\0_FromDexter\3_SyscoPY\1_NLP"
test_path = r"testmanual"
summary = Summary()
d = Directory(test_path, summary)
print(d.jsonfile[0])
d.jsonize("test")

