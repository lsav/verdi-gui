import csv

log = []
for row in csv.reader(open('verdilog.csv', 'rb'), delimiter=','):
    if len(log) == 0:
        row.insert(8, 'BASEPLATE')
        row[-1] = 'COMMENT'
    else:
        if len(row) < 16:
            row.insert(8, 'N/A')
        if len(row) < 15:
            row.append('')
    log.append(row)

with open('converted.csv', 'wb') as newlog:
    writer = csv.writer(newlog, delimiter=',')
    for row in log:
        writer.writerow(row)