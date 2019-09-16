from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from splitter_module import group, member
from datetime import datetime
import matplotlib.pyplot as plt
import os, sys
import pickle
import pandas as pd
import numpy as np
import splitter_module as SM

######################################################################################################################################################################################
#GUI class for Change/Delete group window
class CDGwindow(QWidget):
    def __init__(self):
        super(CDGwindow,self).__init__();
        loadUi('../gui/cdgw.ui',self);
        self.setWindowTitle("Select Group");
        self.setStyleSheet("QWidget {background: "+color+";}");
######################################################################################################################################################################################
#GUI class for payment window
class Pwindow(QWidget):
    def __init__(self):
        super(Pwindow,self).__init__();
        loadUi('../gui/payment.ui',self);
        self.setWindowTitle("Payment");
        self.setStyleSheet("QWidget {background: "+color+";}");
######################################################################################################################################################################################
#GUI class for expense window
class Ewindow(QWidget):
    def __init__(self):
        super(Ewindow,self).__init__();
        loadUi('../gui/expense.ui',self);
        self.setWindowTitle("New Expense");
        self.setStyleSheet("QWidget {background: "+color+";}");
######################################################################################################################################################################################
#GUI class for Empty window
class EmptyWindow(QWidget):
    def __init__(self):
        super(EmptyWindow,self).__init__();
        loadUi('../gui/empty.ui',self);
        self.setStyleSheet("QWidget {background: "+color+";}");
######################################################################################################################################################################################
#GUI class for Settings window
class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow,self).__init__();
        loadUi('../gui/settings.ui',self);
        self.setWindowTitle("Settings");
        self.setStyleSheet("QDialog {background: "+color+";}");
######################################################################################################################################################################################
#GUI class for main window
class mainWindow(QMainWindow):
    def __init__(self):
        #Load UI file
        super(mainWindow, self).__init__();
        loadUi('../gui/splitter.ui',self);

        #Set startup text
        self.setWindowTitle("SpLiTtEr!!!");
        self.disclaimer.setText("Welcome!!!");

        #Mapping button to functions
        self.newGroupButton.clicked.connect(self.newGroup);
        self.changeGroupButton.clicked.connect(self.selectGroup);
        self.deleteGroupButton.clicked.connect(self.selectGroup);
        self.newMemberButton.clicked.connect(self.newMember);
        self.newExpenseButton.clicked.connect(self.newExpense);
        self.newPaymentButton.clicked.connect(self.newPayment);
        self.suggestedPaymentsButton.clicked.connect(self.suggPayments);
        self.statsButton.clicked.connect(self.stats);
        self.settingsButton.clicked.connect(self.settings);
        self.historyButton.clicked.connect(self.history);

        #Set current group name in display
        if(current_group != None):
            self.textBrowser.setText("             "+current_group.name.upper());
    
    #Pre-exit function before closing
    def closeEvent(self, event):
        global color, currency, current_group;
        setting_data = {};
        #Confirmation message box
        reply = QMessageBox.question(self, 'Quit', 'Are You Sure to Quit?', QMessageBox.No | QMessageBox.Yes);
        if reply == QMessageBox.Yes:
            #Store the objects into memory
            with open('../data/record.pkl', 'wb') as output:
                pickle.dump(record, output, pickle.HIGHEST_PROTOCOL);

            #Get the objects to be stored in a dict
            setting_data['current_group'] = current_group;
            setting_data['currency'] = currency;
            setting_data['color'] = color;

            #Store the settings data into memory
            with open("../data/settings.pkl",'wb') as output:
                pickle.dump(setting_data, output, pickle.HIGHEST_PROTOCOL);
            #Close all windows
            plt.close();
            event.accept();
        else:
            #Ignore if No is clicked
            event.ignore();

    #Group creation button API
    def newGroup(self):
        input_window = QInputDialog();
        input_window.setOkButtonText("Create");
        name, okPressed = input_window.getText(self,"New Group","Group Name: ");
        if(okPressed == True):
            #Condition check for empty input
            if (bool(name) == False):
                    self.disclaimer.setText("Please enter a name");
            #Condition check for same group name
            elif SM.isGroupPresent(name, group_list) == True:
                self.disclaimer.setText("Group Already Exists");
            else:
                #Create group API call
                createGroup(name.lower());
                self.disclaimer.setText("Group "+name+" Added Successfully");
    
    #Group change/delete button API
    def selectGroup(self):
        global group_list;
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        else:
            #Load change group UI
            self.nw = CDGwindow();
            #Map buttons to functions depending on the button clicked
            if (self.sender().objectName() == "changeGroupButton"):
                self.nw.buttonBox.accepted.connect(changeGroup);
            if (self.sender().objectName() == "deleteGroupButton"):
                self.nw.buttonBox.accepted.connect(delGroup);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            #Add elements dynamically to the list box
            for ele in group_list:
                self.nw.cb.addItem(ele.name);
            #Display GUI box
            self.nw.show();

    #Member addition button API
    def newMember(self):
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        else:
            input_window = QInputDialog();
            input_window.setOkButtonText("Add");
            name, okPressed = input_window.getText(self,"New Member","Member Name: ");
            if(okPressed == True):
                #Condition check for empty input
                if (bool(name) == False):
                    self.disclaimer.setText("Please enter a name");
                #Condition check for same member name
                elif (SM.isMemberPresent(name.lower(),current_group)):
                    self.disclaimer.setText("Member Already Exists");
                else:
                    #Member addition API call
                    current_group.addMember(name.lower());
                    #Set display element text
                    self.disclaimer.setText(name+" added to Group "+current_group.name);
            self.displaySummary();

    #New expense addition button API
    def newExpense(self):
        #List to hold all credits of all members
        creds = {};
        #Function for placeholder text
        def updatePlaceholder():
            #Read amount entered
            amt = self.nw.amtInput.text();
            #Amount validation
            if (SM.isAmountValid(amt) == True):
                amt = float(amt);
                equal = round(amt/(current_group.size),2);
                #Check if checkbox is selected
                if (window.nw.edCheckBox.isChecked() == True):
                    for (k,v) in self.lines.items():
                        v.setPlaceholderText(str(equal)+"+");
                elif (window.nw.perCheckBox.isChecked() == True):
                    for (k,v) in self.lines.items():
                        v.setPlaceholderText(str(round(100.0/(current_group.size),2))+"%");
                else:
                    for (k,v) in self.lines.items():
                        v.setPlaceholderText(str(equal));
                        

        #Function to change the label when check box is selected
        def state_changed(self):
            #Update plcaeholder text if selection is changed
            updatePlaceholder();
            #If equal+delta is selected
            if (window.nw.sender().objectName() == "edCheckBox"):
                if (window.nw.edCheckBox.isChecked() == True):
                    window.nw.perCheckBox.setChecked(False);
                    window.nw.layoutTitle.setText("Delta Difference");
                    #Set the placeholder text
                    window.nw.amtInput.setPlaceholderText("Amount to be shared equally");
                    return;
            elif (window.nw.sender().objectName() == "perCheckBox"):
                if (window.nw.perCheckBox.isChecked() == True):
                    window.nw.edCheckBox.setChecked(False);
                    window.nw.layoutTitle.setText("Percentage Share");
                    #Clear the placeholder text
                    window.nw.amtInput.setPlaceholderText("");
                    return;
            #If both of the options are not selected
            window.nw.layoutTitle.setText("Individual Share");
            #Clear the placeholder text
            window.nw.amtInput.setPlaceholderText("");
            return;
        
        #Function to perform the pre condition checks and prepare data to send to add expense API
        def getDebits(creds, amt):
            #List to hold all debits of all members
            debts = {};
            #Get the description
            des = self.nw.descripInput.text();
            #Loop through all Line Edits
            for mem in current_group.members:
                #Read data in each Line Edit
                ind_amt = self.lines[mem.name].text();
                #Check for empty LineEdit      
                if (ind_amt == ""):
                    debts[mem.name+"_debit"] = 0;
                #Check for numeric value of the LineEdit
                elif (ind_amt.isnumeric() == True):
                    debts[mem.name+"_debit"] = (-1*float(ind_amt));
                #Invalid amount disclaimer
                else:
                    self.disclaimer.setText("Invalid amount");
                    del(self.nw);
                    return;

            #Check if all LineEdits are empty, if empty then equal share
            if (all(val == 0 for val in list(debts.values()))):
                debts = debts.fromkeys(debts.keys(),(-1*(amt/current_group.size)));

            #Check if the equal+delta option is selected
            if (self.nw.edCheckBox.isChecked() == True):
                #Create a temp dict with equal shares
                temp_debts = dict.fromkeys(debts.keys(),(-1*(amt/current_group.size)));
                #Add all the delta differences to respective members
                for k in debts.keys():
                    temp_debts[k] += debts[k]; 
                #Copy the temp dict to debts
                debts = temp_debts.copy();
                #Modify the amount
                amt = abs(sum(debts.values()));
            #Check if the percentage option is selected
            elif (self.nw.perCheckBox.isChecked() == True):
                #Share the amount percentage-wise
                for key in debts.keys():
                    debts[key] = (debts[key]*amt)/100;

            #Check if all values add up to the entered amount
            if ((abs(abs(sum(list(debts.values()))) - amt) > 0.1) or (abs(sum(list(creds.values())) - amt) > 0.1)):
                msg = QMessageBox();
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Shares do not add up to the total amount given.");
                msg.setWindowTitle("Error!")
                msg.exec_();
            else:
                #Call add expense API by passing all the required processed data
                current_group.addExpense(des, creds, amt, debts);
                self.displaySummary();
                del(self.nw);
                return;

        def getPayers():
            #Lists to hold all checkbox and lineedit objects
            self.checkboxes = [];
            self.lineedits = [];
            #Create a settle window
            self.pw = EmptyWindow();
            self.pw.setWindowTitle("Paid by");
            #Add checkbox for each member
            for mem in current_group.members:
                #Create a checkbox
                self.pw.cb = QCheckBox(self.pw);
                self.pw.cb.setText(mem.name);
                #Create a LineEdit
                self.pw.le = QLineEdit(self.pw);
                self.pw.formLayout.addRow(self.pw.cb,self.pw.le);
                #Collect the checkboxes and lineedits for future reference
                self.checkboxes.append(self.pw.cb);
                self.lineedits.append(self.pw.le);

            #Map buttons and signals to the APIs
            self.pw.buttonBox.accepted.connect(getCreds);
            self.pw.buttonBox.rejected.connect(self.pw.close);
            #Display GUI box
            self.pw.show();

        def getCreds():
            #Get the amount
            amt = self.nw.amtInput.text();
            #Validate the amount
            if (SM.isAmountValid(amt) == False):
                self.disclaimer.setText("Invalid amount");
                del(self.nw);
                return;
            #Convert amount to float
            amt = float(amt);

            #Create a credit library
            for mem in current_group.members:
                creds[mem.name+"_credit"] = 0;

            #Choose only the checkboxes which are selected
            for ele in self.checkboxes:
                if (ele.isChecked() == True):
                    #Get and validate the individual amount
                    num = self.lineedits[self.checkboxes.index(ele)].text();
                    if (SM.isAmountValid(num) == False):
                        self.disclaimer.setText("Invalid amount");
                        del(self.pw);
                        return;
                    else:
                        #Convert the number to float
                        num = float(num);
                        #Update the credit dictionary
                        creds[ele.text()+"_credit"] = num;

            #Get debits API
            getDebits(creds, amt);  
            del(self.pw);
            return;    

        #Variable to hold all lineedits
        self.lines = {};
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        #Check if no members are present in a group
        elif SM.isMemberListEmpty(current_group):
            self.disclaimer.setText("No Members in the group");
        else:
            #Load change group UI
            self.nw = Ewindow();
            self.nw.buttonBox.button(QDialogButtonBox.Ok).setText("Add");
            #Dynamically add row for each member
            for mem in current_group.members:
                #Add LineEdit for each member
                self.lines[mem.name] = QLineEdit();
                self.nw.formLayout.addRow(QLabel(mem.name),self.lines[mem.name]);
                #Assigning placeholder text
                self.nw.amtInput.textChanged.connect(updatePlaceholder);

            #Map button to APIs
            self.nw.buttonBox.accepted.connect(getPayers);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            self.nw.perCheckBox.stateChanged.connect(state_changed);
            self.nw.edCheckBox.stateChanged.connect(state_changed);
            
            #Display GUI box
            self.nw.show();

    #Method to call payment API
    def newPayment(self):
        #Pre process data to call payment API
        def processPayment():
            #Get the payer and check if the member exists
            frm = self.nw.fromInput.currentText().lower();
            if (SM.isMemberPresent(frm, current_group) == False):
                self.disclaimer.setText(frm+" not found in group "+current_group.name);
                del(self.nw);
                return;

            #Get the payee and check if the member exists
            to = self.nw.toInput.currentText().lower();
            if (SM.isMemberPresent(to, current_group) == False):
                self.disclaimer.setText(to+" not found in group "+current_group.name);
                del(self.nw);
                return;

            #validate the amount entered
            amt = self.nw.amtInput.text();
            if (SM.isAmountValid(amt) == False):
                self.disclaimer.setText("Invalid amount");
                del(self.nw);
                return;
            #Convert amount to float
            amt = float(amt);

            #Call payment addition API
            current_group.addPayment(frm,to,amt);
            self.displaySummary();
            #Set display elements after successful transaction
            self.disclaimer.setText("Payment from "+frm+" to "+to+" successfull");
            del(self.nw);

        #Method to update the comboBox with members other than from member
        def updateComboBox():
            #Clear the combo box
            self.nw.toInput.clear();
            #Include all members except the selected one
            for mem in current_group.members:
                if(self.nw.fromInput.currentText().lower() != mem.name):
                    self.nw.toInput.addItem(mem.name);
            
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        #Check if no members are present in a group
        elif SM.isMemberListEmpty(current_group):
            self.disclaimer.setText("No Members in the group");
        else:
            #Open the payment window
            self.nw = Pwindow();
            self.nw.buttonBox.button(QDialogButtonBox.Ok).setText("Pay");
            #Add all member names into the from combobox
            for mem in current_group.members:
                self.nw.fromInput.addItem(mem.name);
            #Initial call to the function
            updateComboBox();
            #Map buttons and signals to the APIs
            self.nw.fromInput.currentIndexChanged.connect(updateComboBox);
            self.nw.buttonBox.accepted.connect(processPayment);
            self.nw.buttonBox.rejected.connect(self.nw.close);
            #Display GUI box
            self.nw.show();

    #Summary display function
    def displaySummary(self):
        disp_data = current_group.summary(); 
        disp = "";
        for (k,v) in disp_data.items():
            disp += (k+"\t\t\t\t     "+str(v)+" "+currency+"\n");
        self.displayText.setText("");
        self.displayText.setText(disp);

    #Settle API
    def suggPayments(self):
        global settle_data;
        self.settle_lines = [];
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        #Check if no members are present in a group
        elif SM.isMemberListEmpty(current_group):
            self.disclaimer.setText("No Members in the group");
        else:
            #Get the settle status
            message, settle_data = current_group.suggestedPayments();
            #Condition check if the accounts are settled
            if (message == None):
                msg = QMessageBox();
                msg.setWindowTitle("Suggested Payments");
                msg.setText("Dues already settled");
                msg.exec_();
            else:
                #Create a settle window
                self.nw = EmptyWindow();
                self.nw.setWindowTitle("Suggested Payments");
                #Add checkbox for each of the transactions
                for ele in settle_data:
                    self.nw.cb = QCheckBox(self.nw);
                    self.nw.cb.setText(ele['From'].upper()+ " pays to "+ele['To'].upper()+"\t "+currency+" "+str(ele['amount']));
                    self.nw.formLayout.addRow(self.nw.cb);
                    #Collect the checkboxes for future reference
                    self.settle_lines.append(self.nw.cb);

                #Map buttons and signals to the APIs
                self.nw.buttonBox.button(QDialogButtonBox.Ok).setText("Settle");
                self.nw.buttonBox.accepted.connect(settleUp);
                self.nw.buttonBox.rejected.connect(self.nw.close);
                #Display GUI box
                self.nw.show();
    
    #Function to plot statistics
    def stats(self):
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        else:
            global file;
            #Read the csv file
            csv_data = SM.getCsvFile(file);
            #Collect all members as labels
            labels = [mem.name for mem in current_group.members];
            #Collect expenses of each member
            expenses = [mem.expenses for mem in current_group.members];
        
            #Pie-Chart
            plt.subplot(221);
            #Add all relevant titles to the plot
            plt.title("Total spends\n"+str(sum(expenses)));
            #Collect the data to be visualised
            sizes = [((val/sum(expenses))*100) for val in expenses];  
            explode = [0.05 for s in sizes];
            #Plotting a pie chart
            plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90);

            #Bar-Graph
            plt.subplot(222);
            #Add all relevant titles to the plot
            plt.title('Expenses per member');
            plt.xlabel('Members');
            plt.ylabel('Expenses');
            #Collect the data to be visualised
            x = np.arange(len(labels));
            plt.xticks(x, labels);
            spends_all = [mem.spend_count for mem in current_group.members];
            #Plot the bars
            plt.bar(x, spends_all, width=0.4, edgecolor='white');

            #Multiple Bar-Graph
            plt.subplot(212);
            #Add all relevant titles to the plot
            plt.title("Personal expenditure");
            plt.xlabel('Months');
            plt.ylabel('Amount');
            #Collect the data to be visualised
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            data = {};
            bars = [];
            x = np.arange(len(months));
            plt.xticks(x, months);
            width = 0.15;
            #Create a dictionary for each member for all months
            for mem in labels:
                data[mem] = {};
                for m in months:
                    data[mem][m] = 0; 
                
            #Loop through all rows and collect expenses for all members in a selected month
            for idx, row in csv_data.iterrows():
                #Get the current month
                curr_month = datetime.strptime(row['Timestamp'],"%Y-%m-%d %H:%M:%S.%f").strftime("%b");
                #Check debit and add it to the dictionary for corresponding month
                for mem in labels:
                    data[mem][curr_month] += abs(row[mem+"_debit"]);
            
            #Position adjust for plotting the bars
            pos_adjust = x-(int(len(labels)/2)*width);
            #Plot all bars and collect then in bars
            for (k,v) in data.items():
                bars.append(plt.bar(pos_adjust,list(v.values()),width,edgecolor='white'));
                pos_adjust += width;

            #Show legend
            plt.legend(bars,labels);

            #Display the plot
            plt.show();

    #Method to apply settings
    def settings(self):
        self.nw = SettingsWindow();
        #Map buttons and signals to the APIs
        self.nw.buttonBox.button(QDialogButtonBox.Ok).setText("Apply");
        self.nw.colorButton.clicked.connect(openColorDialog);
        self.nw.buttonBox.accepted.connect(applySettings);
        self.nw.buttonBox.rejected.connect(self.nw.close);
        #Display GUI box
        self.nw.show();

    #Method to show transaction history
    def history(self):
        #Check if no groups are added
        if (SM.isGroupListEmpty(group_list) == True):
            self.disclaimer.setText("No Groups found!!!");
        else:
            #Create a new window
            self.nw = EmptyWindow();
            self.nw.resize(675,500);
            self.nw.setWindowTitle("Transaction History");
            #Delete unwanted elements
            del(self.nw.formLayout);
            del(self.nw.buttonBox);
            #Create a table widget and a button widget
            self.tableWidget = QTableWidget();
            self.button = QPushButton("OK");
            #Read csv file
            csv_data = SM.getCsvFile(file);
            #Add columns - Date, Description, Amount, Paid by, Shares
            self.tableWidget.setRowCount(csv_data["Timestamp"].count());
            self.tableWidget.setColumnCount(5);
            self.tableWidget.setHorizontalHeaderLabels(["Date","Description","Amount","Paid by","Shares("+",".join([mem.name for mem in current_group.members])+")"]);

            #Loop through all rows and collect expenses for all members in a selected month
            for idx, row in csv_data.iterrows():
                #Local temp varaibles
                shares = [];
                payers = [];
                temp_row = dict(row);
                #Loop through all elements to get the share and amount
                for ele in row:
                    #Enter only if the string is float
                    try:
                        ele = float(ele);
                        #Check only for debit transactions
                        if ele < 0:
                            shares.append(abs(ele));
                        #Check for credit transactions
                        elif ele > 0:
                            #Get payers names
                            p = list(temp_row.keys())[list(temp_row.values()).index(ele)];
                            #Set the element to 0 to avoid duplicate condition
                            temp_row[p] = 0;
                            #Append payers name to the list
                            payers.append(p[:-7]);
                    except:
                        pass;

                #Add the data into the respective fields
                self.tableWidget.setItem(idx,0, QTableWidgetItem(str(row["Timestamp"][:10])));
                self.tableWidget.setItem(idx,1, QTableWidgetItem(row["Description"]));
                self.tableWidget.setItem(idx,2, QTableWidgetItem(str(sum(shares))));
                self.tableWidget.setItem(idx,3, QTableWidgetItem(",".join(payers)));
                self.tableWidget.setItem(idx,4, QTableWidgetItem(",".join([str(s) for s in shares])));

            # Add box layout, add table to box layout and add box layout and button to widget
            self.nw.layout = QVBoxLayout();
            self.nw.layout.addWidget(self.tableWidget);
            self.nw.layout.addWidget(self.button);
            self.nw.setLayout(self.nw.layout);

            #Link button to function
            self.button.clicked.connect(self.nw.close);

            # Show widget
            self.nw.show();

######################################################################################################################################################################################
#Method to create a new group
def createGroup(name):
    global object_count, current_group, file;
    #Creating new group object
    new_Group = group(name);
    #Add group object to the lists
    group_list.append(new_Group);
    #Get appropriate file name for the group
    file = "../reports/"+name+".csv";
    #Add group object and data file into a dictionary for storage
    record[object_count] = new_Group;
    #Update object_counter
    object_count += 1;
    #Create a fresh csv file for the group
    columns = ['Timestamp', 'Description'];
    df = pd.DataFrame(columns=columns);
    df.to_csv(file, index=False);
    #Load the new group as current group
    current_group = new_Group;
    #Set current group name in display text
    window.textBrowser.setText("             "+current_group.name.upper());
    window.displayText.setText("");

#Method to carryout object loading functionality
def initilize_data():
    global group_list, current_group, record, object_count, file, currency, color;
    #Condition check for file existence
    if(os.path.exists('../data/record.pkl')):
        #Read the pickle file
        with open('../data/record.pkl', 'rb') as infile:
            #Try-catch block to handle empty file errors
            try:
                loaded_data = pickle.load(infile);
            except EOFError:
                return;
            #Condition check to handle empty record dictionary
            if bool(loaded_data):
                #Load all data to current session
                group_list = [val for (key,val) in loaded_data.items()];
                record = loaded_data;
                object_count = len(record.keys());

    #Condition check for file existence
    if(os.path.exists('../data/settings.pkl')):
        #Read the pickle file
        with open('../data/settings.pkl', 'rb') as infile:
            #Try-catch block to handle empty file errors
            try:
                loaded_data = pickle.load(infile);
            except EOFError:
                return;
            #Condition check to handle empty record dictionary
            if bool(loaded_data):
                currency = loaded_data['currency'];
                current_group = loaded_data['current_group'];
                color = loaded_data['color'];
                if (current_group != None):
                    file = "../reports/"+current_group.name+".csv";           

#Method to change group context
def changeGroup():
    #Get group name from the GUI
    name = window.nw.cb.currentText().lower();
    global current_group, file, group_list;
    #Change group context
    for obj in group_list:
        if (obj.name == name):
            #Load the respective object
            current_group = obj;
            #Load the working csv file
            file = "../reports/"+name+".csv"; 
            break;
        
    #Close the CDGwindow post operation
    window.nw.close();
    del(window.nw);
    #Set display elements in the GUI
    window.textBrowser.setText("             "+current_group.name.upper());
    window.disclaimer.setText("Group changed to "+current_group.name);
    #Call Summary to update the info
    window.displaySummary();

#Method to delete a group
def delGroup():
    global current_group, file, group_list, record, object_count;
    #Get group name from the GUI
    name = window.nw.cb.currentText().lower();
    #Delete group confirmation message box
    reply = QMessageBox.question(window, 'Delete Group', 'Are You Sure to Delete the group?', QMessageBox.No | QMessageBox.Yes);
    if reply == QMessageBox.Yes:
        #Deleting the group and respective data
        for obj in group_list:
            if (obj.name == name):
                #Remove object from the list
                deleted_obj = group_list.pop(group_list.index(obj));
                #Update the record dictionary
                record = {key: value for key, value in record.items() if value is not deleted_obj};
                #Re-assign appropriate key values
                object_count = 0;
                keys = list(record.keys());
                for i in range(len(keys)):
                    record[object_count] = record.pop(keys[i]);
                    object_count += 1;
                #Delete the group object and csv file
                os.remove("../reports/"+name+".csv");
                del(deleted_obj);
                #Disclaimer if group is empty after deletion
                if (SM.isGroupListEmpty(group_list) == True):
                    current_group = None;
                else:    
                    #Change active group
                    current_group = group_list[0];
                    file = "../reports/"+current_group.name+".csv"; 
                    #current_group.summary();
                    break;
        #Close CDG window
        del(window.nw);
        #Set display element in GUI post deletion
        window.disclaimer.setText("Group "+name+ " deleted");
        if(current_group != None):
            window.textBrowser.setText("             "+current_group.name.upper());
            #Call Summary to update the info
            window.displaySummary();
        else:
            window.textBrowser.setText("");
            window.displayText.setText("");

#Method to settle up
def settleUp():
    global settle_data;
    #Collect indices of payments made
    to_rem = [];
    #Add individual payments to settle all
    for line in window.settle_lines:
        #Add payments to only selected choices
        if (line.isChecked() == True):
            #Get the selected line
            selected_line = settle_data[window.settle_lines.index(line)];
            #Payment API call
            current_group.addPayment(selected_line['From'], selected_line['To'], selected_line['amount']);
            #Track the index to remove later
            to_rem.append(window.settle_lines.index(line));
    #Remove the data after the accounts ahve been settled
    for i in range(len(to_rem)-1,-1,-1):
        del settle_data[to_rem[i]];
        del window.settle_lines[to_rem[i]];
    #Call Summary to update the info
    window.displaySummary();
    #Delete the new window
    del(window.nw);

#Method to open color Dialog
def openColorDialog():
    global color;
    #Get the selected color
    color = (QColorDialog.getColor()).name();

#Method to apply the settings
def applySettings():
    global currency, color;
    #Get the amount debit/credit for each member
    amt_data = list(current_group.summary().values());
    #Check if all accounts are settled
    if (SM.duesSettled(amt_data) == True):
        #Get selected currency
        currency = window.nw.currencyBox.currentText();
        window.disclaimer.setText("Settings Applied");
        window.displaySummary();
    else:
        window.disclaimer.setText("Currency cannot be changed");

    #Apply the color theme
    window.setStyleSheet("QMainWindow {background: "+color+";}");
    #Close and delete the window
    del(window.nw);

######################################################################################################################################################################################
#Main function
if __name__ == '__main__':
    """Global declarations"""
    #Dictionary to hold objects to be saved
    record = {};
    object_count = 0;
    #Group instances monitoring lists
    group_list = [];
    #Active group
    current_group = None;
    currency = "";
    color = "#F0F0F0";
    #Settle data list
    settle_data = [];
    #global object_count, current_group, group_list, group_name_list;
    initilize_data();
    
    #Start GUI
    app = QApplication(sys.argv);
    window = mainWindow();
    #Apply color to the GUI
    window.setStyleSheet("QMainWindow {background: "+color+";}");
    #Display GUI
    window.show();
    #Call summary to initiate display
    if (current_group != None):
        window.displaySummary();
    sys.exit(app.exec_());