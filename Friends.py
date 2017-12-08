#  File: Friends.py
#  Description: This program sumulates a networking site. Users can make new accounts, and make friends with other people.
#  Users input a friend command the program links them with other people
#  Student's Name: Brian Tsai
#  Student's UT EID: byt76
#  Course Name: CS 313E
#  Unique Number: 51465
#
#  Date Created: 11/5/17
#  Date Last Modified: 11/5/17


# Raised when a reference to a person who does not have an account has been made
class UnknownPersonError(Exception):
    def __init__(self, name1, name2 = None):
        self.name1 = name1
        self.name2 = name2

    def getName1(self):
        return self.name1

    def getName2(self):
        return self.name2

# Raised when a reference to the same person in a command has been made
class RedundantPersonError(Exception):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def getName(self):
        return self.name

    def getAction(self):
        return self.action

class Node (object):

   # Create a new node
   def __init__(self,initdata):
      self.data = initdata
      self.next = None

   # Return the node's data
   def getData(self):
      return self.data

   # Return a pointer to the next node
   def getNext(self):
      return self.next

   # Set the data of the node
   def setData(self, newData):
      self.data = newData

   # Set the pointer to the next node
   def setNext(self,newNext):
      self.next = newNext

class LinkedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    # Add a node to the front of the linked list
    def addFirst(self, item):

        temp = Node(item)
        oldHead = self.head

        # Add new node to the front
        if (self.head == None):
            self.head = temp
        else:
            temp.setNext(oldHead)
            self.head = temp

    # Add a node to the end of the linked list
    def addLast(self, item):

        newNode = Node(item)
        currentNode = self.head

        # Add to the front of there are no elements in the list
        if (currentNode == None):
            self.head = newNode
            return

        # Search for the end of the linked list and the new node to the end
        while (currentNode.getNext() != None):
            currentNode = currentNode.getNext()
        currentNode.setNext(newNode)

    # Search the unsorted list for the element
    def findUnordered(self, item):

        currentNode = self.head

        # Iterate through the list searching for the element
        while (currentNode != None):

            # Return true if the element is found
            if (item == str(currentNode.getData())):
                return True
            currentNode = currentNode.getNext()

        # Return false if the element is not found
        return False

    # Remove the element from the linked list if found
    def delete(self, item):

        previousNode = self.head
        currentNode = self.head
        found = False

        # Iterate through the list and search for the element
        while (currentNode != None):
            if (str(currentNode.getData()) == item):
                found = True
                break
            previousNode = currentNode
            currentNode = currentNode.getNext()

        # If the element is found, then remove it
        if (found):

            # Remove from the front
            if (currentNode == self.head):
                self.head = currentNode.getNext()

            # Remove from the end
            elif (currentNode.getNext() == None):
                previousNode.setNext(None)

            # Remove from in between
            else:
                previousNode.setNext(currentNode.getNext())
            return True

        else:
            return False

    def getItem(self, item):

        currentNode = self.head

        # Iterate through the list searching for the element
        while (currentNode != None):

            # Return true if the element is found
            if (item == str(currentNode.getData())):
                return currentNode.getData()
            currentNode = currentNode.getNext()

        # Return false if the element is not found
        return None

    # Return the length of the list
    def getLength(self):

        current = self.head
        count = 0

        # Count the number of items in the list
        while (current != None):
            current = current.getNext()
            count += 1
        return count

        # Return the string representation of the linked list
    def __str__(self):
        list = []
        current = self.head

        # Append all node data to a list
        while (current != None):
            list.append(str(current.getData()))
            current = current.getNext()

        # Format the nodes into a string representation
        string = ' '.join(list)
        string = '[ ' + string + ' ]'
        return str(string)



class User:

    # Create a new user
    def __init__(self, name):
        self.name = name
        self.friends = LinkedList()

    # Add a new friend to the user's friend list
    def addFriend(self, friend):
        self.friends.addFirst(friend)

    # Remove a person from the user's friend list
    def deleteFriend(self, friend):
        self.friends.delete(friend)

    # Return whether a user has a certain friend
    def hasFriend(self, friend):
        return self.friends.findUnordered(friend)

    # Return whether a person has any friends
    def hasFriends(self):
        return not self.friends.isEmpty()

    # Return a a friend from the user's friend list
    def getFriend(self, friend):
        return self.friends.getItem(friend)

    # Return whether the user is friends with a certain person
    def areFriends(self, friend):
        return self.friends.findUnordered(friend)

    # Return a list of the user's friends
    def listFriends(self):
        return str(self.friends)

    # Return a string representation of this user
    def __str__(self):
        return str(self.name)



# Command to make a new user account
def addUser(output, people, name):

    # Create a new account for a new user
    if (not people.findUnordered(name)):
        people.addFirst(User(name))
        output.write("    " + name + " now has an account.\n\n")
    else:
        output.write("    A person with name " + name + " already exists.\n\n")



# Command to add a friend to a user
def friendPerson(output, people, user, person):

    # Raise exceptions if necessary
    if (user == person): raise RedundantPersonError(user, "friend")
    if (not people.findUnordered(user) or not people.findUnordered(person)): raise UnknownPersonError(user, person)

    # Add the person to the user's friend list if they aren't friends already
    currentUser = people.getItem(user)
    if (not currentUser.hasFriend(person)):
        newFriend = people.getItem(person)
        currentUser.addFriend(newFriend)
        newFriend.addFriend(currentUser)
        output.write("    " + user + " and " + person + " are now friends.\n\n")
    else:
        output.write("    " + user + " and " + str(person) + " are already friends.\n\n")



# Command to unfriend a person
def unfriendPerson(output, people, user, person):

    # Raise exceptions if necessary
    if (user == person): raise RedundantPersonError(user, "unfriend")
    if (not people.findUnordered(user) or not people.findUnordered(person)): raise UnknownPersonError(user, person)

    # Unfriend a person if they are not friends already
    currentUser = people.getItem(user)
    if (currentUser.hasFriend(person)):
        oldFriend = people.getItem(person)
        currentUser.deleteFriend(person)
        oldFriend.deleteFriend(user)
        output.write("    " + user + " and " + person + " are no longer friends.\n\n")
    else:
        output.write("    " + user + " and " + person + " aren't friends, so you can't unfriend them.\n\n")


# Command to list all of the user's friends
def listFriends(output, people, user):

    # Raise exceptions if necessary
    if (not people.findUnordered(user)): raise UnknownPersonError(user)

    # Output a string representation of a user's friend list if they have any
    currentUser = people.getItem(user)
    if (currentUser.hasFriends()):
        output.write("    " + currentUser.listFriends() + "\n\n")
    else:
        output.write("    " + user + " has no friends.\n\n")


# Command to check the status of two people
def queryFriends(output, people, user, person):

    # Raise exceptions if necessary
    if (user == person): raise RedundantPersonError(user, "query")
    if (not people.findUnordered(user) or not people.findUnordered(person)): raise UnknownPersonError(user, person)


    # Output whether two people are friends
    currentUser = people.getItem(user)
    if (currentUser.areFriends(person)):
        output.write("    " + user + " and " + person + " are friends.\n\n")
    else:
        output.write("    " + user + " and " + person + " are not friends.\n\n")


# Command to exit the program
def exit(output):
    output.write("    Exiting...\n")


def main():

    # Open buffers for editing
    input = open("FriendData.txt", "r")
    output = open("FriendOutput.txt", "w")

    # Create a new linked list of people who have user accounts
    people = LinkedList()
    for line in input:
        line = line.strip()
        output.write("--> " + line + "\n")
        line = line.split()

        # Parse all the commands in the stream
        try:
            command = line[0]
            if (command == "Person"):
                user = line[1]
                addUser(output, people, user)
            elif (command == "Friend"):
                user = line[1]
                person = line[2]
                friendPerson(output, people, user, person)
            elif (command == "Unfriend"):
                user = line[1]
                person = line[2]
                unfriendPerson(output, people, user, person)
            elif (command == "List"):
                user = line[1]
                listFriends(output, people, user)
            elif (command == "Query"):
                user = line[1]
                person = line[2]
                queryFriends(output, people, user, person)
            elif (command == "Exit"):
                exit(output)
                break

        # Exception to catch a reference to a person who has not made an account
        except UnknownPersonError as unknownPerson:
            if (not people.findUnordered(unknownPerson.getName1())):
                output.write("    A person with name " + unknownPerson.getName1() + " does not currently exist.\n\n")
            if (unknownPerson.getName2() != None and not people.findUnordered(unknownPerson.getName2())):
                output.write("    A person with name " + unknownPerson.getName2() + " does not currently exist.\n\n")

        # Exception to catch a reference to a person who has been referred to twice in a command
        except RedundantPersonError as redudantPerson:
            output.write("    A person cannot " + redudantPerson.getAction() + " him/herself.\n\n")
        output.flush()

    # Close the buffer
    input.close()
    output.close()

main()