#!/usr/bin/python3
"""command line interpreter to test my work"""
import cmd
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review
from models.city import City
from models import storage


class HBNBCommand(cmd.Cmd):
    """created the class which is to be used for cmd."""

    prompt = '(hbnb) '
    classes = {
        "BaseModel": BaseModel,
        "Amenity": Amenity,
        "Place": Place,
        "User": User,
        "State": State,
        "Review": Review,
        "City": City
    }

    def do_quit(self, line):
        """quit commmand: - used to quit the console"""
        return True

    def do_EOF(self, line):
        """EOF command: - quits console with ctrl + d"""
        return True

    def emptyline(self):
        """command for an empty line."""
        pass

    def do_create(self, line):
        """creates a new class instance of basemode.l"""
        line.split(" ")
        if len(line) == 0:
            print("** class name missing **")

        elif line not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        else:
            insta = HBNBCommand.classes[line]()
            insta.save()
            print(insta.id)

    def do_show(self, line):
        """Show the string representation of an instance of a class created:"""
        k = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")

        elif k[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(k) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(k[0], k[1]) not in storage.all().keys():
            print("** no instance found **")

        else:
            g = storage.all()["{}.{}".format(k[0], k[1])]
            print(g)

    def do_destroy(self, line):
        """Destroys the Instance of a class created"""
        k = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")

        elif k[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(k) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(k[0], k[1]) not in storage.all().keys():
            print("** no instance found **")

        else:
            del(storage.all()["{}.{}".format(k[0], k[1])])
            storage.save()

    def do_all(self, line):
        """Show all instances of classes created by class or not"""
        k = line.split(" ")
        objs = storage.all()
        lists = []
        if len(line) == 0:
            for key, val in objs.items():
                lists.append(val.__str__())
        elif k[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        else:
            for key, val in objs.items():
                j = key.split(".")
                if k[0] == j[0]:
                    lists.append(val.__str__())
        print(lists)

    def do_update(self, line):
        """update:
        Updates an instance based on the class name and
        id by adding or updating attribute
        (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com
        """
        k = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")

        elif k[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(k) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(k[0], k[1]) not in storage.all().keys():
            print("** no instance found **")

        elif len(k) == 2:
            print("** attribute name missing **")

        elif len(k) == 3:
            print("** value missing **")

        elif len(k) == 4:
            g = storage.all()["{}.{}".format(k[0], k[1])]
            if k[2] in g.__class__.__dict__.keys() and\
                    type(g.__class__.__dict__[k[2]] in ({str, float, int})):
                type_val = type(g.__class__.__dict__[k[2]])
                g.__dict__[k[2]] = type_val(k[3])
            else:
                g.__dict__[k[2]] = k[3]

        storage.save()

    def default(self, line):
        """to retrieve all instances of a class by using: <class name>.all()"""
        k = line.split(".")
        if len(line) == 0:
            return
        else:
            args_class = k[0]
            if args_class in HBNBCommand.classes:
                if len(k) == 2:
                    if k[1] == "all()":
                        HBNBCommand.do_all(self, args_class)
                    elif k[1] == "count()":
                        HBNBCommand.do_count(self, args_class)
                    elif k[1][:4] == "show":
                        info = k[1]
                        l_id = info[6:-2]
                        lined = str(args_class) + " " + str(l_id)
                        HBNBCommand.do_show(self, lined)
                    elif k[1][:7] == "destroy":
                        info = k[1]
                        l_id = info[8: -2]
                        lined = str(args_class) + " " + str(l_id)
                        HBNBCommand.do_destroy(self, lined)
                    elif k[1][:6] == "update":
                        info = k[1]
                        args = info[7: -1]
                        listd = args.split(', ')
                        l_id = listd[0][1: -1]
                        if listd[1][0] == "{":
                            dictd = args.split(', {')
                            dct = '{' + dictd[1]
                            dicted = eval(dct)
                            for key, val in dicted.items():
                                lined = str(args_class) + " " + str(l_id)\
                                    + " " + str(key) + " " + str(val)
                                HBNBCommand.do_update(self, lined)
                        else:
                            attr = listd[1][1: -1]
                            if listd[2][0] == '"' and listd[2][-1] == '"':
                                val = str(listd[2][1: -1])
                            else:
                                val = listd[2]
                            lined = str(args_class) + " " + str(l_id)\
                                + " " + str(attr) + " " + val
                            HBNBCommand.do_update(self, lined)

                    else:
                        pass
                else:
                    pass

    def do_count(self, line):
        """count number of objects of a class"""
        k = line.split(" ")
        if len(line) == 0:
            return
        else:
            count = 0
            if k[0] in HBNBCommand.classes:
                for key in storage.all().keys():
                    j = key.split(".")
                    if k[0] == j[0]:
                        count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
