# Final Project CMPSC 131
# Project collaborators: Vishnu Sree Peram, Shwetak Mattagajasingh, Timothy Schum, Yelly Seck, Fionah Gronski

# Question 2
def popular():
    file = open('librarylog.txt','r')
    librarylog = file.readlines()
    file.close()

    file = open('booklist.txt','r')
    booklist = file.readlines()
    file.close()

    n = 0
    for line in librarylog:
        line = line.strip().split('#')
        if len(line) <= 1:
            break
        if int(line[1]) > n:
            n = int(line[1])

    d = {}
    for line in booklist:
        line = line.strip().split('#')
        book = line[0]
        number = int(line[1])
        d[book] = [n*number]

    file = open('librarylog.txt','r')
    librarylog = file.readlines()
    file.close()
    for line in librarylog:
        line = line.strip().split('#')
        if line[0] == 'A':
            k = n-int(line[1])+1
            if line[2] in d:
                d[line[2]] = [d[line[2]][0]+k]
            else:
                d[line[2]] = [k]

    file = open('librarylog.txt', 'r')
    librarylog1 = file.readlines()
    file.close()

    file = open('librarylog.txt','r')
    librarylog2 = file.readlines()
    file.close()

    for line in librarylog1:
        i = 0
        line = line.strip().split('#')
        if len(line) <=1:
            break
        if line[0] == 'B':
            day = int(line[1])
            name = line[2]
            book = line[3]
            borrowed_for = line[4]
            for entry in librarylog2:
                entry = entry.strip().split('#')
                if len(entry) == 1:
                    if len(d[book]) == 2:
                        d[book][1] = d[book][1] + (n-day+1)
                        break
                    elif len(d[book]) == 1:
                        d[book].append(n-day+1)
                        break
                if entry[0] == 'R' and int(entry[1]) > day and entry[2] == name and entry[3] == book:
                    i = int(entry[1])-day
                    if len(d[book]) == 2:
                        d[book][1] = d[book][1] + i
                        break
                    elif len(d[book]) == 1:
                        d[book].append(i)
                        break

    return d


d = popular()
for key, value in d.items():
    print('{} days borrowed out of {} {}'.format(value[1],value[0],key))


# Question 3
def borrowratio():
    d = popular()
    for key, value in d.items():
        ratio = (value[1]/value[0])*100
        print('{} with usage {}'.format(key,ratio))

borrowratio()

# Question 4

lst1 = []
lst2 = []
d = popular()
for key,value in d.items():
    ratio = (value[1]/value[0])*100
    lst1.append(ratio)
    lst2.append(value[1])

lst1.sort()    # borrow ratio
lst2.sort()    # most borrowed
print(lst1)
print(lst2)
most_borrowed = []
ratio = []
d = popular()
for i in lst2:
    for key,value in  d.items():
        if value[1] == i:
            most_borrowed.append(key)

for i in lst1:
    for key,value in d.items():
        if (value[1]/value[0])*100 == i:
            ratio.append(key)

print(ratio)
print(most_borrowed)

# Question 5
def fines():

    def booklist():
        file = open('booklist.txt', 'r')
        booklist = file.readlines()
        file.close()
        return booklist

    def librarylog():
        file = open('librarylog.txt', 'r')
        librarylog = file.readlines()
        file.close()
        return librarylog

    b = booklist()
    restricted = []
    unrestricted = []
    fine = 0
    for line in b:
        line = line.strip().split('#')
        if line[2] == 'FALSE':
            unrestricted.append(line[0])
        elif line[2] == 'TRUE':
            restricted.append(line[0])

    di = {}
    l = librarylog()
    for line in l:
        line = line.strip().split('#')
        if len(line) <= 1: break
        if line[0] == 'B':
            if line[2] in di:
                continue
            else:
                di[line[2]] = 0

    l = librarylog()
    for line in l:
        line = line.strip().split('#')

        if len(line) <= 1 :
            break

        if line[0] == 'A':
            if line[2] in restricted:
                restricted.append(line[2])
            elif line[2] in unrestricted:
                unrestricted.append(line[2])
            else:
                unrestricted.append(line[2])

    for na in di:
        l = librarylog()
        fine = 0
        for line in l:
            line = line.strip().split('#')

            if len(line) <= 1:
                break

            if line[0] == 'P' and line[2] == na:
                fine -= int(line[3])

            if line[0] == 'B' and line[2] == na:
                name = line[2]
                book = line[3]
                total = int(line[1]) + int(line[4])

                k = librarylog()

                for entry in k :
                    entry = entry.strip().split('#')

                    if len(entry) <= 1:
                        break

                    if int(entry[1]) < int(line[1]):
                        continue

                    if entry[0] == 'R' and entry[2] == name and entry[3] == book:
                        if int(entry[1]) <= total:
                            break

                        else:
                            p = int(entry[1]) - total

                            if book in restricted:
                                fine += p*5

                            elif book in unrestricted:
                                fine += p*1

        di[na] = fine
    return di

print(fines())

# Question 1

def borrow(student,book,day,borrow_days) :

    def booklist():
        file = open('booklist.txt', 'r')
        booklist = file.readlines()
        file.close()
        return booklist

    def librarylog():
        file = open('librarylog.txt', 'r')
        librarylog = file.readlines()
        file.close()
        return librarylog

    # check the restriction conditions
    b = booklist()
    for line in b:
        line = line.strip().split('#')
        if line[0] == book:
            restriction = line[2]
        else: continue

        if restriction == 'TRUE':
            if int(borrow_days) > 7 :
                return 'Restricted book. Cannot be borrowed for more than 7 days'
        elif restriction == 'FALSE':
            if int(borrow_days) > 28 :
                return 'Any book cannot be borrowed for more than 28 days'

    # check if there's a copy in the library
    copies = 0
    b = booklist()
    for line in b:
        line = line.strip().split('#')
        if line[0] == book:
            copies = int(line[1])
            break

    l = librarylog()
    for line in l:
        line = line.strip().split('#')
        if int(line[1]) <= int(day):
            if line[0] == 'B' and line[3] == book:
                copies -= 1
            elif line[0] == 'R' and line[3] == book:
                copies +=1
            elif line[0] == 'A' and line[2] == book:
                copies +=1
        else:
            break

    if copies < 1:
        return 'Book currently unavailable'

    # check if the student has already borrowed maximum (3) number of books
    books_borrowed = 0
    l = librarylog()
    for line in l:
        line = line.strip().split('#')
        if int(line[1]) <= int(day):
            if line[0] == 'B' and line[2] == student:
                books_borrowed +=1
            elif line[0] == 'R' and line[2] == student:
                books_borrowed -=1

        else:
            if books_borrowed >= 3:
                return 'Cannot borrow more than 3 books'
            break

    # check if the student has any pending fines
    b = booklist()
    restricted = []
    unrestricted = []
    fine = 0
    for line in b:
        line = line.strip().split('#')
        if line[2] == 'FALSE':
            unrestricted.append(line[0])
        elif line[2] == 'TRUE':
            restricted.append(line[0])

    l = librarylog()
    for line in l:
        line = line.strip().split('#')
        if int(line[1]) > int(day) :
            break
        if line[0] == 'A':
            if line[2] in restricted:
                restricted.append(line[2])
            elif line[2] in unrestricted:
                unrestricted.append(line[2])
            else:
                unrestricted.append(line[2])

    l = librarylog()
    k = librarylog()
    for line in l:
        line = line.strip().split('#')

        if int(line[1]) > day:
            break

        if line[0] == 'B' and line[2] == student:
            total = int(line[1]) + int(line[4])
            borbook = line[3]
            if total > day:
                continue

            for entry in k:
                entry = entry.strip().split('#')
                if int(entry[1]) > day:
                    break
                if entry[0] == 'R' and entry[2] == student and entry[3] == borbook:
                    p = int(entry[1]) - total
                    if p < 0 :
                        break
                    elif entry[3] in restricted:
                        fine += 5*p
                        break
                    elif entry[3] in unrestricted:
                        fine += 3*p
                        break
                elif entry[1] == day:
                    p = int(entry[1]) - total
                    if p < total:
                        break
                    elif borbook in restricted:
                        fine += 5*p
                        break
                    elif borbook in unrestricted:
                        fine += 3*p
                        break


    if fine > 0:
        return 'pending fines {}, cannot borrow'.format(fine)

    return 'You can borrow the book'

k = input('Press ENTER to start entering information to check if someone can borrow a book')
n = input('Enter the name of the person: ')
b = input('Enter the name of the book: ')
d = int(input('Enter how many days the person wants to borrow the book: '))
h = int(input('Enter the day on which the student wants to borrow the book: '))

print(borrow(n,b,h,d))