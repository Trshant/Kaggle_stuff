
def measureSbgrade(value):
	grades = ["","a","b","c","d","e","f"]
	grades_num = grades.index(value[0])
	return int(grades_num) * int(value[1])


print measureSbgrade('d4')