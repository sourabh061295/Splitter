import pandas as pd
from datetime import datetime

######################################################################################################################################################################################
#Creating a class of people which hold their name and amount
class member:
    def __init__(self,name):
        self.name = name;
        self.expenses = 0;
        self.spends = 0;
        self.spend_count = 0;
######################################################################################################################################################################################
#Class group contains all data of the group
class group:
    def __init__(self, name):
        self.name = name;                                                           #Name of the group
        self.members = [];                                                          #Contains people objects
        self.size = 0;                                                              #Size of the group

    #Method to add new member to the group
    def addMember(self, name):
        #Update file name
        file_name = "./reports/"+self.name+".csv";
        #Add the new member people object to the list
        self.members.append(member(name));
        #Get current members in the group
        csv_data = pd.read_csv(file_name);
        temp_row = list(csv_data);
        #Add new member name to list
        temp_row.append(name);
        #Adding timestamp column and Description column for temperoray row
        if not("Timestamp" in temp_row):
            temp_row.insert(0,"Timestamp");
        if not("Description" in temp_row):
            temp_row.insert(1,"Description");
        #Update the csv file with the new member
        csv_data[name+"_debit"] = 0;
        csv_data[name+"_credit"] = 0;
        df = pd.DataFrame(csv_data);
        df.to_csv(file_name, index=False);
        #Update the group size
        self.size += 1;
        return;

    #Method to add new expense in the group
    def addExpense(self, des, creds, amt, debts):
        #Get all names of the members
        name_list = [mem.name for mem in self.members];
        #Update file name
        file_name = "./reports/"+self.name+".csv";
        #Add timestamp to the transaction
        timestamp = datetime.now();
        #Create a temporary dictionary
        temp_dict = {'Timestamp':[timestamp],'Description':[des]};
        #Add all debits in the dataframe
        for k in debts.keys():
            #Add to dictionary write to csv
            temp_dict[k] = [debts[k]];
            #Extract name
            name = k[:-6].lower();
            #Update the member object parameters
            self.members[name_list.index(name)].spends += 0;
            self.members[name_list.index(name)].expenses += abs(debts[k]);
        #Add all credits in the dataframe
        for k in creds.keys():
            #Add to dictionary write to csv
            temp_dict[k] = [creds[k]];
            #Extract name
            name = k[:-7].lower();
            #Update the member object parameters
            self.members[name_list.index(name)].spends += abs(creds[k]);
            #Increment spend count only if the member has spent
            if (creds[k] > 0):
                self.members[name_list.index(name)].spend_count += 1;

        #Read the csv file
        csv_data = pd.read_csv(file_name);
        #Convert the dictionary to a dataframe
        df = pd.DataFrame(temp_dict);
        csv_data = pd.concat([csv_data, df], sort=False);
        #Write to the csv file
        df = pd.DataFrame(csv_data);
        df.to_csv(file_name, index=False);
        return;


    #Method to add payment
    def addPayment(self,frm,to,amt):
        #Update file name
        file_name = "./reports/"+self.name+".csv";
        #Read the csv file
        csv_data = pd.read_csv(file_name);
        #Create a temporary dictionary
        temp_dict = dict.fromkeys(csv_data.keys(),[0]);
        #Add timestamp and description to the payment transaction
        temp_dict['Timestamp'] = datetime.now();
        temp_dict['Description'] = "Payment";
        #Update the details for the payee and the payer
        temp_dict[frm+"_debit"] = [(-1*amt)];
        temp_dict[to+"_credit"] = [amt];
        #Convert the dictionary to a dataframe
        df = pd.DataFrame(temp_dict);
        csv_data = pd.concat([csv_data, df], sort=False);
        #Write to the csv file
        df = pd.DataFrame(csv_data);
        df.to_csv(file_name, index=False);
        return;

    #Method to calculate summary
    def summary(self):
        #Create an empty dictionary
        info = {};
        #Create a key for each member
        for mem in self.members:
            info[mem.name] = mem.spends - mem.expenses;
        #Update file name
        file_name = "./reports/"+self.name+".csv";
        #Read the csv file
        csv_data = pd.read_csv(file_name);
        #Iterate over all rows
        for idx, row in csv_data.iterrows():
            #Pick transactions tagged as payments
            if (row['Description'] == 'Payment'):
                #For all members, add the credits and subtract the debits
                for mem in self.members:
                    info[mem.name] -= row[mem.name+"_credit"];
                    info[mem.name] += abs(row[mem.name+"_debit"]); 
        #Return the updated dictionary
        return info;

    #Method to calculate suggested payments
    def suggestedPayments(self):
        #Local variables to use
        message = "";
        settle_data = [];
        settle_count = 0;
        #Get all names of the members
        name_list = [mem.name for mem in self.members];
        #Get the amount debit/credit for each member
        amt_data = list(self.summary().values());
        #Check if all accounts are settled
        if (duesSettled(amt_data) == True):
            message = None;
        else:
            #Run this loop until all accounts have been settled
            while(settle_count != self.size):
                #Reset the settle count
                settle_count = 0;
                #Pick the maximum value in the list
                maxi = max(amt_data);
                #Pick the mininimum value in the list
                mini = min(amt_data);
                #Case where the only the payer is settled
                if((maxi + mini) >= 0):
                    #Print and store the payment info in the list
                    message += (name_list[amt_data.index(mini)].upper()+" pays to -----> "+name_list[amt_data.index(maxi)].upper()+": Rs "+str(abs(mini))+"\n");
                    settle_data.append({'From':name_list[amt_data.index(mini)], 'To': name_list[amt_data.index(maxi)], 'amount': abs(mini)});
                    #Update the transaction
                    amt_data[amt_data.index(maxi)] = round((amt_data[amt_data.index(maxi)] - abs(mini)),2);
                    amt_data[amt_data.index(mini)] = 0;
                #Case where the only the payee is settled 
                else:
                    #Print and store the payment info in the list
                    message += (name_list[amt_data.index(mini)].upper()+" pays to -----> "+name_list[amt_data.index(maxi)].upper()+": Rs "+str(abs(maxi))+"\n");
                    settle_data.append({'From':name_list[amt_data.index(mini)], 'To': name_list[amt_data.index(maxi)], 'amount': abs(maxi)});
                    #Update the transaction
                    amt_data[amt_data.index(maxi)] = 0;
                    amt_data[amt_data.index(mini)] = round((amt_data[amt_data.index(mini)] + maxi),2);
                #Count the number of accounts settled
                for val in amt_data:
                    if(val == 0):
                        settle_count += 1;
        
        #Return the Payment suggestions to display
        return message, settle_data;
######################################################################################################################################################################################
#Utility APIs
#API to check if a member already exists in the group
def isMemberPresent(name, group):
    retval = False;
    gr_mem = [mem.name for mem in group.members];
    if name in gr_mem:
        retval = True;
    return retval;

#API to check if a group already exists in the list
def isGroupPresent(name, gr_list):
    retval = False;
    gr_list = [g.name for g in gr_list];
    if name in gr_list:
        retval = True;
    return retval;

#API to validate the amount
def isAmountValid(amt):
    retval = False;
    if (amt.isnumeric() == True):
        retval = True;
        #Checking for positive values only
        if float(amt) < 0:
            retval = False; 
    return retval;

#API to check if all dues are settled
def duesSettled(amt_list):
    retval = False;
    if (all(val == 0 for val in amt_list)):
        retval = True;
    return retval;

#API to check if the group list is empty
def isGroupListEmpty(gr_list):
    retval = False;
    if len(gr_list) == 0:
        retval = True;
    return retval;

#API to check if the member list is empty
def isMemberListEmpty(group):
    retval = False;
    if len(group.members) == 0:
        retval = True;
    return retval;

#API to get the csv data as a dataframe
def getCsvFile(file_name):
    return pd.read_csv(file_name);

        
