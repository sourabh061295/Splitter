from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from splitter import group, people
import matplotlib.pyplot as plt
import csv
import os, time, sys
import pickle
from goto import with_goto

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

    #Method to add new member to the group
    def addMember(self, name):
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
        print("member addition succesfull");

    def addExpense(self):
        des = window.nw.descripInput.text();
        payee = window.nw.paidInput.text().lower();
        if not(payee in self.name_list):
            window.disclaimer.setText(payee+" not found in group "+current_group.name);
            del(window.nw);
            return;

        amt = window.nw.amtInput.text();
        if (amt.isnumeric() == False):
            window.disclaimer.setText("Invalid amount");
            del(window.nw);
            return;
        else:
            amt = float(amt);
            ind_amt = [];
            #Condition check for invalid amount
            if amt <= 0:
                window.disclaimer.setText("Invalid amount");
                del(window.nw);
                return;
            
            timestamp = time.time();
            equal_flag = True;
            balance = 0; 
            for mem in self.name_list:
                if (bool(window.lines[mem].text())):
                    equal_flag = False;
                    break;

            if(equal_flag):
                ind_amt = [round(amt/(self.size), 2) for i in range(self.size)];
            else:
                for mem in self.name_list:
                    data = window.lines[mem].text();
                    if data == "":
                        ind_amt.append(0);
                    else:
                        ind_amt.append(float(data));

            if not (abs(sum(ind_amt) - amt) <= 0.1):
                msg = QMessageBox();
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Shares do not add up to the total amount given.");
                msg.setWindowTitle("Error!")
                msg.exec_();
            else:
                #Calculate the amount to be paid to the payee
                for person in self.name_list:
                    if not (payee == person):
                        balance += ind_amt[self.name_list.index(person)];
                        ind_amt[self.name_list.index(person)] *= -1;
                #Assign the amount to be paid to the payer
                ind_amt[self.name_list.index(payee)] = balance;

                #Adding timestamp and expense description to the transaction
                ind_amt.insert(0,timestamp);
                ind_amt.insert(1,des);
                #Note the transaction into the csv file
                with open(file,'a', newline = '') as csv_file:
                    name_writer = csv.writer(csv_file)
                    name_writer.writerow(ind_amt);

                #Call summary() to store the amount of each individual into their respective people objects
                self.summary();
                print("Expense addition successful");
                del(window.nw);
                return;

    #Method to add payment
    def addPayment(self,flag = -1):
        global settle_data;
        if (flag < 0):
            frm = window.nw.fromInput.text().lower();
            if not(frm in self.name_list):
                window.disclaimer.setText(frm+" not found in group "+current_group.name);
                del(window.nw);
                return;

            to = window.nw.toInput.text().lower();
            if not(to in self.name_list):
                window.disclaimer.setText(to+" not found in group "+current_group.name);
                del(window.nw);
                return;

            amt = window.nw.amtInput.text();
            if (amt.isnumeric() == False):
                window.disclaimer.setText("Invalid amount");
                del(window.nw);
                return;
        else:
            frm = settle_data[flag]['From'];
            to = settle_data[flag]['To'];
            amt = settle_data[flag]['amount'];

        amt = float(amt);
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
        if (flag < 0):
            del(window.nw);
        window.disclaimer.setText("Payment from "+frm+" to "+to+" successfull");
        print("Payment successfull");
        return;

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
        disp = "";
        for (k,v) in info.items():
            disp += (k+"\t\t\t\t       "+str(v)+"\n");
            window.displayText.setText("");
            window.displayText.setText(disp); 
        #Return payment summary
        print("Summary updated");

    #Method to display suggested payments
    @with_goto
    def suggestedPayments(self, startup = 0):
        global settle_data;
        #List of to-be settled amounts
        amt_list = [ele.amount for ele in self.members];
        if startup == 1:
            goto .start;
        msg = QMessageBox();
        msg.setWindowTitle("Suggested payments")
        message = "";
        
        if (all(val == 0 for val in amt_list)):
            message = "Dues already settled";
        else:  
            label .start
            #Variable to check if all accounts have been settled up
            settle_count = 0;
            settle_data = [];
            #Run this loop until all accounts have been settled
            while(settle_count < self.size):
                if (all(val == 0 for val in amt_list)):
                    break;
                #Pick the maximum value in the list
                maxi = max(amt_list);
                #Pick the mininimum value in the list
                mini = min(amt_list);
                #Case where the only the payer is settled
                if((maxi + mini) >= 0):
                    #Print and store the payment info in the list
                    message += (self.name_list[amt_list.index(mini)].upper()+" pays to -----> "+self.name_list[amt_list.index(maxi)].upper()+": Rs "+str(abs(mini))+"\n");
                    settle_data.append({'From':self.name_list[amt_list.index(mini)], 'To': self.name_list[amt_list.index(maxi)], 'amount': abs(mini)});
                    #Update the transaction
                    amt_list[amt_list.index(maxi)] = round((amt_list[amt_list.index(maxi)] - abs(mini)),2);
                    amt_list[amt_list.index(mini)] = 0;
                #Case where the only the payee is settled 
                else:
                    #Print and store the payment info in the list
                    message += (self.name_list[amt_list.index(mini)].upper()+" pays to -----> "+self.name_list[amt_list.index(maxi)].upper()+": Rs "+str(abs(maxi))+"\n");
                    settle_data.append({'From':self.name_list[amt_list.index(mini)], 'To': self.name_list[amt_list.index(maxi)], 'amount': abs(maxi)});
                    #Update the transaction
                    amt_list[amt_list.index(maxi)] = 0;
                    amt_list[amt_list.index(mini)] = round((amt_list[amt_list.index(mini)] + maxi),2);
                #Increement settle count if any account has been settled
                for v in amt_list:
                    if(v == 0):
                        settle_count += 1;
        if startup == 0:
            msg.setText(message);
            msg.exec_();
        print("Suggested payments updated successfully");

    #Method to settle up
    def settleUp(self):
        global settle_data;
        to_rem = [];
        #Add individual payments to settle all
        for l in window.settle_lines:
            if (l.isChecked() == True):
                self.addPayment(window.settle_lines.index(l));
                to_rem.append(window.settle_lines.index(l));
        for idx in to_rem:
            del settle_data[idx];
            del window.settle_lines[idx];
        print("Settle complete");
        del(window.nw);

######################################################################################################################################################################################
#Method to create a new group
def createGroup(name):
    global object_count, current_group, file;
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
    print("group addition success");
    window.textBrowser.setText("             "+current_group.name.upper());

#Method to change group context
def changeGroup():
    name = window.nw.cb.currentText().lower();
    global current_group, file, group_list;
    #Change group context
    for obj in group_list:
        if (obj.name == name):
            #Load the respective object
            current_group = obj;
            #Load the working csv file
            file = "./reports/"+name+".csv"; 
            break;
    window.nw.close();
    del(window.nw);
    window.textBrowser.setText("             "+current_group.name.upper());
    window.disclaimer.setText("Group changed to "+current_group.name);
    current_group.summary();

    
#Method to delete a group
def delGroup():
    global current_group, file, group_name_list, group_list, record, object_count;
    name = window.nw.cb.currentText().lower();
    reply = QMessageBox.question(window, 'Delete Group', 'Are You Sure to Delete the group?', QMessageBox.No | QMessageBox.Yes);
    if reply == QMessageBox.Yes:
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
                os.remove("./reports/"+name+".csv");
                del(deleted_obj);
                #Disclaimer if group is empty after deletion
                if (len(group_list) == 0):
                    current_group = "";
                else:    
                    #Change active group
                    current_group = group_list[0];
                    file = "./reports/"+current_group.name+".csv"; 
                    current_group.summary();
                    break;
        window.disclaimer.setText("Group "+name+ " deleted");
        del(window.nw);
        if(current_group != ""):
            window.textBrowser.setText("             "+current_group.name.upper());
        else:
            window.textBrowser.setText("");
            window.displayText.setText("");

######################################################################################################################################################################################
#GUI code
class CGwindow(QWidget):
    def __init__(self):
        super(CGwindow,self).__init__();
        loadUi('./gui/cgw.ui',self);
        self.setWindowTitle("Select Group");

class Pwindow(QWidget):
    def __init__(self):
        super(Pwindow,self).__init__();
        loadUi('./gui/payment.ui',self);
        self.setWindowTitle("Payment");

class Ewindow(QWidget):
    def __init__(self):
        super(Ewindow,self).__init__();
        loadUi('./gui/expense.ui',self);
        self.setWindowTitle("New Expense");

class SettleWindow(QWidget):
    def __init__(self):
        super(SettleWindow,self).__init__();
        loadUi('./gui/settle.ui',self);
        self.setWindowTitle("Settle Up");

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__();
        loadUi('./gui/splitter.ui',self);

        self.setWindowTitle("SpLiTtEr!!!");
        self.disclaimer.setText("Welcome!!!");
        #Mapping button to functions
        self.newGroupButton.clicked.connect(self.newGroup);
        self.changeGroupButton.clicked.connect(self.selectGroup);
        self.deleteGroupButton.clicked.connect(self.deleteGroup);
        #self.statsButton.clicked.connect(self.stats);
        self.newMemberButton.clicked.connect(self.newMember);
        self.newExpenseButton.clicked.connect(self.newExpense);
        self.settleUpButton.clicked.connect(self.settle);
        self.newPaymentButton.clicked.connect(self.newPayment);
        self.suggPaymentButton.clicked.connect(self.suggPayments);

        if(current_group != ""):
            self.textBrowser.setText("             "+current_group.name.upper());

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are You Sure to Quit?', QMessageBox.No | QMessageBox.Yes);
        if reply == QMessageBox.Yes:
            with open('record.pkl', 'wb') as output:
                pickle.dump(record, output, pickle.HIGHEST_PROTOCOL)
            event.accept()
        else:
            event.ignore()

    def newGroup(self):
        name, okPressed = QInputDialog.getText(self,"New Group","Group Name: ");
        if(okPressed == True):
            #Condition check for same group name
            if(name.lower() in group_name_list):
                self.disclaimer.setText("Group Already Exists");
            else:
                createGroup(name.lower());
                self.disclaimer.setText("Group "+name+" Added Successfully");

    def selectGroup(self):
        global group_list, group_name_list;
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            self.nw = CGwindow();
            self.nw.buttonBox.accepted.connect(changeGroup);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            for ele in group_name_list:
                self.nw.cb.addItem(ele);
            self.nw.show();
        
    def deleteGroup(self):
        global group_list, group_name_list;
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            self.nw = CGwindow();
            self.nw.buttonBox.accepted.connect(delGroup);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            for ele in group_name_list:
                self.nw.cb.addItem(ele);
            self.nw.show();
    
    def newMember(self):
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            name, okPressed = QInputDialog.getText(self,"New Member","Member Name: ");
            if(okPressed == True):
                #Condition check for same group name
                if(name.lower() in current_group.name_list):
                    self.disclaimer.setText("Member Already Exists");
                else:
                    current_group.addMember(name.lower());
                    self.disclaimer.setText(name+" added to Group "+current_group.name);
        current_group.summary();
    
    def newPayment(self):
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            self.nw = Pwindow();
            self.nw.buttonBox.accepted.connect(current_group.addPayment);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            self.nw.show();

    def newExpense(self):
        def default():
            amt = self.nw.amtInput.text();
            if (amt.isnumeric() == True):
                amt = float(amt);
                equal = round(amt/(current_group.size),2);
                for (k,v) in self.lines.items():
                    v.setPlaceholderText(str(equal));

        self.lines = {};
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            self.nw = Ewindow();
            for mem in current_group.name_list:
                self.lines[mem] = QLineEdit();
                self.nw.formLayout.addRow(QLabel(mem),self.lines[mem]);
                self.nw.amtInput.textChanged.connect(default);

            self.nw.buttonBox.accepted.connect(current_group.addExpense);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            self.nw.show();
    
    def suggPayments(self):
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            current_group.suggestedPayments();
    
    def settle(self):
        global settle_data;
        self.settle_lines = [];
        if (len(group_list) == 0):
            self.disclaimer.setText("No Groups found!!!");
        else:
            amt_list = [ele.amount for ele in current_group.members];
            if (all(val == 0 for val in amt_list)):
                msg = QMessageBox();
                msg.setWindowTitle("Settle Up");
                msg.setText("Dues already settled");
                msg.exec_();
            else:
                self.nw = SettleWindow();
                for ele in settle_data:
                    self.nw.cb = QCheckBox(self.nw);
                    self.nw.cb.setText(ele['From'].upper()+ " pays to "+ele['To'].upper()+"\t Rs. "+str(ele['amount']));
                    self.nw.formLayout.addRow(self.nw.cb);
                    self.settle_lines.append(self.nw.cb);

                self.nw.buttonBox.accepted.connect(current_group.settleUp);
                self.nw.buttonBox.rejected.connect(self.nw.close);
                self.nw.show();
        
################################################################################################################################################################################
#Method to carryout object loading functionality
def initilize_data():
    global group_list, current_group, record, object_count, group_name_list, file;
    #Condition check for file existence
    if(os.path.exists('record.pkl')):
        #Read the pickle file
        with open('record.pkl', 'rb') as infile:
            #Try-catch block to handle empty file errors
            try:
                loaded_data = pickle.load(infile);
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
                current_group.suggestedPayments(1);

#Main function
if __name__ == '__main__':
    """Global declarations"""
    #Dictionary to hold objects to be saved
    record = {};
    object_count = 0;
    #Group instances monitoring lists
    group_name_list = [];
    group_list = [];
    #Active group
    current_group = "";
    #Settle data list
    settle_data = [];
    #global object_count, current_group, group_list, group_name_list;
    initilize_data();
    
    app = QApplication(sys.argv);
    window = mainWindow();
    if(current_group != ""):
        current_group.summary();
    window.show();
    sys.exit(app.exec_());
