#!/usr/bin/env python3

csvfile = "fields.csv"
svgfile = "template.svg"
outbase = "out"

svg = ''.join(open(svgfile, 'r').readlines())
csv = open(csvfile, 'r').readlines()


fields = []
for field in csv[0].split(','):
	field = field.strip()
	if field[0] == '"': field = field[1:]
	if field[-1] == '"': field = field[:-1]
	fields.append(field)

print("Fields in '" + csvfile + "': " + repr(fields))

count = 0
while True:
	found = True
	for field in fields:
		idx = svg.find('#' + field + str(count+1) + '#')
		if idx == -1:
			found = False
			break
	if not found:
		break
	count += 1

print("Found " + str(count) + " sets of fields in '" + svgfile + "'.")

nextOut = svg
nextIndex = 1

outIndex = 1

def writeFile():
	global nextOut
	global nextIndex
	global outIndex
	outfile = outbase + str(outIndex) + ".svg"
	print("Writing '" + outfile + "'...")
	with open(outfile, 'w') as f:
		f.write(nextOut)
	nextOut = svg
	nextIndex = 1
	outIndex += 1
	
for line in csv[1:]:
	if nextIndex > count:
		writeFile()
	values = []
	for value in line.split(','):
		value = value.strip()
		if value[0] == '"': value = value[1:]
		if value[-1] == '"': value = value[:-1]
		values.append(value)
	assert(len(values) == len(fields))
	for i in range(0, len(values)):
		find = '#' + fields[i] + str(nextIndex) + '#'
		replace = values[i]
		nextOutReplaced = nextOut.replace(find,replace)
		assert(nextOutReplaced != nextOut)
		nextOut = nextOutReplaced
	nextIndex += 1

if nextIndex > 1:
	writeFile()
