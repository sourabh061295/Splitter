#Import Packages
from goto import with_goto
import csv
import pickle
import time
import os

######################################################################################################################################################################################
#Creating a class of people which hold their name and amount
class people:
        def __init__(self,name):
            self.name = name;                                                       #Name of the member
            self.amount = 0;                                                        #Contains the amount due-ed/owe-ed by the member
######################################################################################################################################################################################


######################################################################################################################################################################################
#Class group contains all data of the group
class group:
    def __init__(self, name):
        self.members = [];                                                          #Contains people objects
        self.name_list = [];                                                        #Contains name of all members of a group
        self.size = 0;                                                              #Size of the group
        self.name = name;                                                           #Name of the group

    #Method to add an expense in the group
    @with_goto
    def addExpense(self,des,name,amount):
        #Condition check for invalid amount
        if amount <= 0:
            return "AMOUNT_INVALID";

        #Condition check for invalid name
        if not(name in self.name_list):
            return "NAME_DOESNT_EXIST";

        timestamp = time.time();                                                            #Timestamp of transaction
        #Getting the individual share
        label .acc_input
        print("Enter individual share in the order "+str(self.name_list)+" with spaces or else press E for equal share among all.");
        data = input();
        balance = 0;                                                                        #Holds the amount to be paid to the payer
        if(data.upper() == 'E'):
            ind_amt = [round(amount/(self.size), 2) for i in range(self.size)];             #Amount divided equally
        else:
            data = data.split();                                                            #Convert string to a list
            #Check for numeric data
            try:                                                       
                ind_amt = [float(d) for d in data];                                         #Convert all elements to float
            except ValueError:
                print("INVALID NUMERIC VALUES");
                print("PLEASE TRY AGAIN.");
                goto .acc_input

            #Condition check for insufficient or excess data input
            if (len(ind_amt) != self.size):
                print("Insufficient/Excess of input data.");
                print("PLEASE TRY AGAIN.");
                goto .acc_input
            #Condition check for shares equalling total amount
            if (sum(ind_amt) != amount):
                print("Shares do not add up to the total amount given.");
                print("PLEASE TRY AGAIN.");
                goto .acc_input
        #Calculate the amount to be paid to the payee
        for person in self.name_list:
            if not (name == person):
                balance += ind_amt[self.name_list.index(person)];
                ind_amt[self.name_list.index(person)] *= -1;
        #Assign the amount to be paid to the payer
        ind_amt[self.name_list.index(name)] = balance;

        #Adding timestamp and expense description to the transaction
        ind_amt.insert(0,timestamp);
        ind_amt.insert(1,des);
        #Note the transaction into the csv file
        with open(file,'a', newline = '') as csv_file:
            name_writer = csv.writer(csv_file)
            name_writer.writerow(ind_amt);

        #Call summary() to store the amount of each individual into their respective people objects
        self.summary();
        return "SUCCESS";

    #Method to add new member to the group
    def addMember(self, name):
        #Condition check for same name
        if(name in self.name_list):
            return "NAME_ALREADY_EXISTS";
        
        #Add the new member people object to the list
        self.members.append(people(name));
        #Add the new member name to the list
        self.name_list.append(name);
        #Adding timestamp column and Description column for temperoray row
        temp_row = [ele for ele in self.name_list];
        if not("Timestamp" in self.name_list):
            temp_row.insert(0,"Timestamp");
        if not("Description" in self.name_list):
            temp_row.insert(1,"Description");
        #Reading csv file 
        with open(file, 'r+') as data_file:
            reader = csv.reader(data_file);
            lines = list(reader);
            #Write to the csv file with the new added member
            with open(file,'w', newline = '') as csv_file:
                name_writer = csv.writer(csv_file)
                #Condition check for empty csv file
                if (len(lines) == 0):
                    name_writer.writerow(temp_row);
                else:
                    lines[0]= temp_row;
                    for i in range(1,len(lines)):
                        lines[i].append(0);
                    for line in lines:
                        name_writer.writerow(line)
        #Update the size of the group
        self.size = len(self.members);
        return (str(self.size)+" member/s in the group");

    #Method to add payment
    def addPayment(self, frm, to, amt):
        payment_amt = [];
        for mem in self.name_list:
            if(mem == frm):
                payment_amt.append(amt);
            elif(mem == to):
                payment_amt.append((-1*amt));
            else:
                payment_amt.append(0);
        #Adding timestamp and description to the transaction
        timestamp = time.time();
        payment_amt.insert(0,timestamp);
        payment_amt.insert(1,"Payment");
        #Note the transaction into the csv file
        with open(file,'a', newline = '') as csv_file:
            name_writer = csv.writer(csv_file)
            name_writer.writerow(payment_amt);
        #Call summary() to store the amount of each individual into their respective people objects
        self.summary();
        return "SUCCESS";
    
    #Method to get size of the group
    def getSize(self):
        return (self.size);

    #Method which returns the due summary of all members
    def summary(self):
        info = {};
        #Reading csv file
        with open(file, 'r') as data_file:
            reader = csv.reader(data_file);
            lines = list(reader);
            #Pop out the header
            header = lines.pop(0);
            #Pop out the timestamp placeholder
            header.pop(0);
            #Pop out the description placeholder
            header.pop(0);
            #Traversing through all members
            for i in range(self.size):
                total = 0;
                #Adding up all the entries in a column
                for row in lines:
                    total += float(row[i+2]);                                           #i+2 eliminates usage of timestamp and description for calculation
                #Float variable rounding off
                info[header[i]] = round(total, 2);
                #Update the amount due-ed/owe-ed into the object
                self.members[i].amount = round(total, 2);
            #Return payment summary
            return info;

    #Method to display suggested payments
    def suggestedPayments(self):
        global settle_data;
        #Variable to check if all accounts have been settled up
        settle_count = 0;
        #List of to-be settled amounts
        amt_list = [ele.amount for ele in self.members];
        #Run this loop until all accounts have been settled
        while(settle_count < self.size):
            #Pick the maximum value in the list
            maxi = max(amt_list);
            #Pick the mininimum value in the list
            mini = min(amt_list);
            #Case where the only the payer is settled
            if((maxi + mini) >= 0):
                #Print and store the payment info in the list
                print(self.name_list[amt_list.index(mini)].upper()+" pays to -----> "+self.name_list[amt_list.index(maxi)].upper()+": Rs "+str(abs(mini)));
                settle_data.append({'From':self.name_list[amt_list.index(mini)], 'To': self.name_list[amt_list.index(maxi)], 'amount': abs(mini)});
                #Update the transaction
                amt_list[amt_list.index(maxi)] = round((amt_list[amt_list.index(maxi)] - abs(mini)),2);
                amt_list[amt_list.index(mini)] = 0;
            #Case where the only the payee is settled 
            else:
                #Print and store the payment info in the list
                print(self.name_list[amt_list.index(mini)].upper()+" pays to -----> "+self.name_list[amt_list.index(maxi)].upper()+": Rs "+str(abs(maxi)));
                settle_data.append({'From':self.name_list[amt_list.index(mini)], 'To': self.name_list[amt_list.index(maxi)], 'amount': abs(maxi)});
                #Update the transaction
                amt_list[amt_list.index(maxi)] = 0;
                amt_list[amt_list.index(mini)] = round((amt_list[amt_list.index(mini)] + maxi),2);
            #Increement settle count if any account has been settled
            for v in amt_list:
                if(v == 0):
                    settle_count += 1;
        return "SUCCESS";

    #Method to settle up
    def settleUp(self):
        global settle_data;
        #Condition check if suggested payments is executed previously
        if (len(settle_data) == 0):
            self.suggestedPayments();
        #Add individual payments to settle all
        for d in settle_data:
            self.addPayment(d['From'],d['To'],d['amount']); 
        return "SUCCESS"

######################################################################################################################################################################################

#Method to create a new group
def createGroup(name):
    global object_count, current_group, file;
    #Condition checkn for same group name
    if(name in group_name_list):
        return "GROUP_ALREADY_EXISTS"
    else:
        #Creating new group object
        newGroup = group(name);
        #Add group name and object to the lists
        group_name_list.append(name);
        group_list.append(newGroup);
        #Get appropriate file name for the group
        file = "./reports/"+name+".csv";
        #Add group object and data file into a dictionary for storage
        record[object_count] = newGroup;
        #Create a fresh csv file for the group
        with open(file, "w") as my_empty_csv:
            pass;
        current_group = newGroup;
    #Return the group object
    return "SUCCESS";

#Method to carryout object saving functionality
def preExit():
    with open('record.pkl', 'wb') as output:
        pickle.dump(record, output, pickle.HIGHEST_PROTOCOL)

#Method to carryout object loading functionality
def init():
    global group_list, current_group, record, object_count, group_name_list, file;
    #Condition check for file existence
    if(os.path.exists('record.pkl')):
        #Read the pickle file
        with open('record.pkl', 'rb') as input:
            #Try-catch block to handle empty file errors
            try:
                loaded_data = pickle.load(input);
            except EOFError:
                return;
            #Condition check to handle empty record dictionary
            if bool(loaded_data):
                #Load all data to current session
                group_list = [val for (key,val) in loaded_data.items()];
                current_group = group_list[0];
                record = loaded_data;
                object_count = len(record.keys());
                group_name_list = [obj.name for obj in group_list];
                file = "./reports/"+current_group.name+".csv";
        
#Method to change group context
def changeGroup(name):
    global current_group, file, group_name_list, group_list;
    #Condition check for group presence
    if not(name in group_name_list):
        return "GROUP_DOESNT_EXIST";
    #Change group context
    for obj in group_list:
        if (obj.name == name):
            #Load the respective object
            current_group = obj;
            #Load the working csv file
            file = "./reports/"+name+".csv"; 
            break;
    return "SUCCESS";

#Method to get list of groups
def getGroups():
    global group_name_list;
    #Condition check for empty list
    if not bool(group_name_list):
        return "EMPTY";
    #Return group name list
    return group_name_list;

#Method to get list of members
def getMembers():
    global group_list, current_group;
    #Condition check for no groups
    if (current_group == 0):
        return "NO GROUPS FOUND";
    #Condition check for empty list
    if not bool(current_group.name_list):
        return "EMPTY";
    #Return member list
    return current_group.name_list;

#Method to delete a group
def delGroup(name):
    global current_group, file, group_name_list, group_list, record, object_count;
    #Deleting the group and respective data
    for obj in group_list:
        if (obj.name == name):
            #Remove object from the list
            deleted_obj = group_list.pop(group_list.index(obj));
            #Remove group name from the list
            group_name_list.remove(deleted_obj.name);
            #Update the record dictionary
            record = {key: value for key, value in record.items() if value is not deleted_obj};
            #Re-assign appropriate key values
            object_count = 0;
            keys = list(record.keys());
            for i in range(len(keys)):
                record[object_count] = record.pop(keys[i]);
                object_count += 1;
            #Delete the group object and csv file
            os.remove(file)
            del(deleted_obj);
            #Disclaimer if group is empty after deletion
            if (len(group_list) == 0):
                current_group = 0;
            else:    
                #Change active group
                current_group = group_list[0];
                file = "./reports/"+current_group.name+".csv"; 
            break;
    return ("\""+name+"\" DELETED SUCCESSFULLY");

#Start-up screen
def menuDisplay():
    global current_group;
    print("/************************************************************************************************************/");
    print("/                                   Welcome to SpLiTtEr!!!                                                   /");
    print("/************************************************************************************************************/");
    print("/*                                        LEGEND                                                            */");
    print("/*----------------------------------------------------------------------------------------------------------*/");
    print("/*                 KEY                      |                    FUNCTION                                   */");
    print("/*----------------------------------------------------------------------------------------------------------*/");
    print("/*                  G                       |                  Add new group                                */");
    print("/*                  M                       |                  Add new member                               */");
    print("/*                  E                       |                   Add expense                                 */");
    print("/*                  P                       |                   Add payment                                 */");
    print("/*                  C                       |                  Change group                                 */");
    print("/*                  L                       |                Get list of groups                             */");
    print("/*                  A                       |       Get list of memebers in the active group                */");
    print("/*                  D                       |                   Delete group                                */");
    print("/*                  S                       |                     Summary                                   */");
    print("/*                  U                       |                    Settle up                                  */");
    print("/*                  X                       |                      Exit                                     */");
    print("/*----------------------------------------------------------------------------------------------------------*/");
    #Condition check for active group status
    if(current_group != 0):
        print("Active group: "+current_group.name.upper());
    else:
        print("No group selected.");

#Main function
def main():
    global object_count, current_group, group_list, group_name_list;
    init();
    #Forever loop
    while(True):
        menuDisplay();
        #Getting the action to be performed
        key = input("Enter your choice: ");
        #Group creation
        if(key.upper() =='G'):
            name = input("Group Name: ");
            resp = createGroup(name.lower());
            if(resp == "SUCCESS"):
                object_count += 1;
            print(resp);
        #Member Addition
        if(key.upper() =='M'):
            if (current_group == 0):
                print("No group selected");
            else:
                name = input("Member Name: ");
                resp = current_group.addMember(name.lower());
                print(resp);
        #Expense addition
        if(key.upper() =='E'):
            if (current_group == 0):
                print("No group selected");
            else:
                des = input("Expense description: ");
                name = input("Paid by: ");
                amt = input("Amount paid: ");
                #Condition check for numeric input
                if(amt.isnumeric() == False):
                    print("AMOUNT_INVALID");
                else:
                    resp = current_group.addExpense(des,name.lower(),float(amt));
                    print(resp);
        #Add a payment
        if(key.upper() =='P'):
            if (current_group == 0):
                print("No group selected");
            else:
                frm = input("From: ");
                to = input("To: ");
                if ((not(frm in current_group.name_list)) or (not(to in current_group.name_list))):
                    print("NAME_DOESNT_EXIST");
                else:
                    amt = input("Amount: ");
                    #Condition check for numeric input
                    if(amt.isnumeric() == False):
                        print("AMOUNT_INVALID");
                    else:
                        resp = current_group.addPayment(frm,to,float(amt));
                        print(resp);
        #Getting Payment summary
        if(key.upper() =='S'):
            if (current_group == 0):
                print("No group selected");
            else:
                resp = current_group.summary();
                print(resp);
        #Suggested Payments
        if(key.upper() == 'T'):
            if (current_group == 0):
                print("No group selected");
            else:
                resp = current_group.suggestedPayments();
                print(resp);
        #Change group
        if(key.upper() =='C'):
            group = input("Change to group: ");
            resp = changeGroup(group.lower());
            print(resp);
        #Get list of groups
        if(key.upper() =='L'):
            resp = getGroups();
            print(resp);
        #Get list of members in current group
        if(key.upper() =='A'):
            resp = getMembers();
            print(resp);
        #Settle all dues
        if(key.upper() =='U'):
            resp = current_group.settleUp();
            print(resp);
        #Delete group
        if(key.upper() =='D'):
            group = input("Group to delete: ");
            #Condition check for empty list
            if (len(group_list) == 0):
                print("GROUP_LIST_EMPTY");
            #Condition check for group absence
            if not(group in group_name_list):
                print("GROUP_DOESNT_EXIST");
            else:
                req = input("Are you sure you want to delete group (y/n): ");
                if (req.lower() == 'y'):
                    resp = delGroup(group.lower());
                print(resp);
        #Exit
        if(key.upper() =='X'):
            preExit();
            print("GOODBYE!!!!");
            print("Have a great day ;-)");
            break;

#Dictionary to hold objects to be saved
record = {};
object_count = 0;
#Group instances monitoring lists
group_name_list = [];
group_list = [];
#Active group
current_group = 0;
#Settle data list
settle_data = [];

if __name__ == '__main__':
    main()


