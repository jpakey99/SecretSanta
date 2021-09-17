import random
import smtplib, ssl


def get_people():
    file = open('list.csv')
    file.readline()
    spending_limit = 0
    people = []
    for line in file:
        line_list = line.split(',')
        spending_limit = line_list[2]
        people.append((line_list[0], line_list[1].strip(' '), line_list[3].strip('\n')))
    return spending_limit, people


def assign_people(people):
    # a list of pairs of people.  (person buying, person receiving)
    pairs = []
    buying_people = people.copy()
    for person in people:
        find_buyer = True
        tries = 0
        while find_buyer and tries < 5:
            random_selection = random.randint(0,len(buying_people)-1)
            if person != buying_people[random_selection]:
                pairs.append((buying_people[random_selection], person))
                buying_people.remove(buying_people[random_selection])
                find_buyer = False
            tries += 1
        if tries == 5:
            return
    return pairs


def send_amail(assignments, spending_limit):
    port = 465  # For SSL
    password = open('password.txt').readline()
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("secretsantajpa@gmail.com", password)
        sender_email = 'secretsantajpa@gmail.com'
        for assignment in assignments:
            buyer, buyer_email, ideas = assignment[0]
            receiver, receiver_email, ideas = assignment[1]
            message = """\
Subject: Secret Santa

{}, You will be buying for {}!  Here is a list of ideas {}.  Remember, the spending limit is ${}.
""".format(buyer, receiver, ideas, spending_limit)
            print(message)
            server.sendmail(sender_email, buyer_email, message)


if __name__ == '__main__':
    spending_limit, people = get_people()
    assignments = None
    while assignments is None:
        assignments = assign_people(people)
    send_amail(assignments, spending_limit)
