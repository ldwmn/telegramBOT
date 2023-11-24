def write_to_db(userid, name, surname, birthday):

    with open('test.txt', 'a') as file:
        file.write(str(userid))
        file.write('\t')
        file.write(name)
        file.write('\t')
        file.write(surname)
        file.write('\t')
        file.write(str(birthday))
        file.write('\n')

if __name__ == '__main__':
    write_to_db("t", "k", "6")