import psycopg2
import random
import sys
import PySimpleGUI as sg
import time


uppers = "ABCDEFGHIJGLMNOPQRSTUVWXYZ"
lowers = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
symbols = "~!@#$%^&*()-=+[{}]\\|<,.>/?"

list_of_characters = [uppers, lowers, numbers, symbols]


def gen_pass(pass_length):
    if pass_length.isnumeric():
        pass_length = int(pass_length)
    else:
        pass_length = 14

    final_pass = ""
    o_to_three = [0, 1, 2, 3]
    random.shuffle(o_to_three)

    final_pass += random.choice(list_of_characters[o_to_three[0]])
    final_pass += random.choice(list_of_characters[o_to_three[1]])
    final_pass += random.choice(list_of_characters[o_to_three[2]])
    final_pass += random.choice(list_of_characters[o_to_three[3]])

    for i in range(pass_length - 4):
        final_pass += random.choice(list_of_characters[random.randrange(0, 4)])

    return final_pass


def init_db(curs):

    query = '''
    CREATE TABLE IF NOT EXISTS credentials(
        cid SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        site VARCHAR(100) NOT NULL
    );
    '''
    curs.execute(query)


def add_pass(curs, values, new_pass):
    username = values['-USERNAME-']
    site = values['-SITE-']

    query = f'''
    INSERT INTO credentials(username,password,site) VALUES(
        '{username}',
        '{new_pass}',
        '{site}'
    );
    '''

    curs.execute(query)

    sg.PopupQuickMessage("[+] Credentials successfully added to the database!")


def conn_to_db():  # return a cursor

    sg.theme('BlueMono')
    layout = [
        [sg.Text("Access to your personal database", font="Calibri 24")],
        [sg.Text("Host:", font="Calibri 20"), sg.InputText(key='-HOST-', size=(20, 4))],
        [sg.Text("Database:", font="Calibri 20"), sg.InputText(key='-DB-', size=(20, 4))],
        [sg.Text("User:", font="Calibri 20"), sg.InputText(key='-USER-', size=(20, 4))],
        [sg.Text("Password:", font="Calibri 20"), sg.InputText(key='-PASS-', size=(20, 4))],
        [sg.Button('Login'), sg.Button('Exit')]
    ]

    window = sg.Window(title="Access to your Database", layout=layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Login':
            try:
                conn = psycopg2.connect(host=values['-HOST-'], database=values['-DB-'], user=values['-USER-'], password=values['-PASS-'])
                curs = conn.cursor()

                sg.PopupQuickMessage(f"[+] Correctly connected to {values['-DB-']}, welcome {values['-USER-']}!")

                init_db(curs)

                time.sleep(3)
                window.close()

                return curs, conn

            except psycopg2.DatabaseError as err:
                sg.Popup(f"[-] Error: {err}")
                sys.exit(1)


def main():
    curs, connection = conn_to_db()

    sg.theme('DarkBrown5')
    layout = [
        [sg.Text("Welcome to Andrea Coppari's Password Generator!", font="Calibri 24")],
        [sg.Text("Site:", font="Calibri 18")], [sg.Input(key='-SITE-', size=(35, 2))],
        [sg.Text("Username:", font="Calibri 18")], [sg.Input(key='-USERNAME-', size=(35, 2))],
        [sg.Button("Generate random password"), sg.T('Length:', font='Calibri 14'),
         sg.Input(key='-LENGTH-', size=(8, 2))],
        [sg.Button('Save'), sg.Button('Exit')]
    ]
    window = sg.Window(title="Password Generator by Andrea Coppari", layout=layout)
    new_pass = ""

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == "Generate random password":
            new_pass = gen_pass(values['-LENGTH-'])
            sg.Popup(f"New password: {new_pass}")
        if event == 'Save':
            add_pass(curs, values, new_pass)

    window.close()

    curs.execute("SELECT * FROM credentials;")
    print(curs.fetchall())

    curs.close()
    connection.close()


main()
