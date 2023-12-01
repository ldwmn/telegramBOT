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


def find_user_by_id(userid):
    with open('test.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split('\t')
            if user_data[0] == str(userid):
                return user_data
def find_user_by_name(name):
    with open('test.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split('\t')
            if user_data[1] == str(name):
                return user_data

if __name__ == '__main__':
    write_to_db('132758', 'Тима', 'Калинин', '13.24.8751')
    print(find_user_by_id(1327181968))
    print(find_user_by_name('гоша'))