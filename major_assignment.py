import enum
from datetime import datetime, timedelta
import uuid




class Account:
	transactions = []
	def __init__(self,account_number,first_name,last_name,tz_offset,balance):
		self.account_number = account_number
		self.first_name = first_name
		self.last_name = last_name
		self.tz_offset = tz_offset
		self.balance = balance
	def change_fname(self,to_change):
		self.first_name = to_change

	def change_lname(self,to_change):
		self.last_name = to_change

	def deposit(self,to_add):
		self.balance += float(to_add)
		self.transactions.append(Transaction(amount = to_add, account_number = self.account_number, operation_type = OperationType.Deposit, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))

	def withdraw(self,to_sub):
		if(self.balance-to_sub<0):
			self.transactions.append(Transaction(amount = to_sub, account_number = self.account_number, operation_type = OperationType.Operation_denied, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))
			print ("Transaction declined.")
		else:
			self.balance -= to_sub
			self.transactions.append(Transaction(amount = to_sub, account_number = self.account_number, operation_type = OperationType.Withdrawal, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))
			print("Withdrawal complete.")


	def deposit_interest(self):
		self.balance += self.balance*0.04
		self.transactions.append(Transaction(amount = self.balance*0.04, account_number = self.account_number, operation_type = OperationType.Interest_deposit, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))
		print("Interest deposited")

	def find_transaction(self,confirmation_code):
		flag = False
		for elem in self.transactions:
			if(elem.confirmation_code == confirmation_code):
				elem.output()
				flag = True
		if(flag==False):
			print ("Invalid confirmation code.")

	def show_transactions(self):
		print("\n\n\nYour transactions:")
		for elem in self.transactions:
			elem.output()


	def show_account(self):
		print(("\n\nAccount ID -> {}\nAccount holder name -> {}\nBalance -> {}\nTime offset -> {}\n\n").format((self.account_number),(self.first_name+" "+self.last_name),(self.balance),(self.tz_offset)))

class OperationType(enum.Enum):
	Deposit = 1
	Withdrawal = 2
	Interest_deposit = 3
	Operation_denied = 4


class Transaction:
	def __init__(self,amount,account_number,operation_type,time_utc,tz_offset):
		self.amount = amount
		self.account_number = account_number
		self.operation_type = operation_type
		self.time_utc = time_utc
		self.tz_offset = tz_offset
		self.transaction_id =  uuid.uuid4() #will always be unique
		self.confirmation_code = "{}-{}-{}".format(self.account_number,time_utc,self.transaction_id) #concat of the three vals to ensure uniqueness

	def output(self):
		tz = TimeZone(self.tz_offset)
		print(("\nTransaction amount -> {}\nAccount number -> {}\nOperation type -> {}\nTime(UTC) -> {}\nTime(Pref. time zone) -> {}\nTransaction id -> {}\nConfirmation code -> {}\n\n\n").format(str(self.amount),str(self.account_number),str(self.operation_type),str(self.time_utc),str(tz.get_pref(self.time_utc)),str(self.transaction_id),str(self.confirmation_code)))

class TimeZone:
	#tz_offset is in hours
	def __init__(self,tz_offset):
		self.tz_offset = tz_offset
	def get_pref(self,time):
		return time+timedelta(hours=self.tz_offset)


def check_name(name):
	if(len(name)<2):
		print("That does not look like a valid name. ")
		return False
	return True


def check_account(acc):
	if(len(acc)!=13):
		print("That does not look like a valid account number. ")
		print("Number must have 13 digits. ")
		return False
	return True


def check_balance(b):
	if(int(b)<0):
		print("Balance cannot be negative. ")
		return False
	return True

def check_tz(b):
	if(b>24):
		print("Offset cannot exceed 24 hours.")
		return False
	return True

def accountSetup():
	f_name = str(input("Enter first name:"))
	while ((check_name(f_name))==False):
		f_name = input("Enter first name:")
	l_name = input("Enter last name:")
	while ((check_name(l_name))==False):
		l_name = input("Enter last name:")
	acc = input("Enter account number:")
	while ((check_account(acc))==False):
		acc = input("Enter account number:")
	balance = input("Enter account balance:")
	while ((check_balance(balance))==False):
		balance = input("Enter account balance:")
	offset = float(input("Enter preferred offset:"))
	while ((check_tz(offset))==False):
		offset = input("Enter preferred offset:")
	thisAccount = Account(acc,f_name,l_name,offset,float(balance))
	print("Account created!")
	return thisAccount

acc = accountSetup()
while True:
	print("MENU")
	print("1. change first name")
	print("2. change last name")
	print("3. make deposit")
	print("4. withdraw")
	print("5. deposit interest")
	print("6. find transactions")
	print("7. show transactions")
	print("8. show account")
	print("9. exit")
	x = int(input("Enter your choice:"))
	if(x==1):
		str_1 = (input("Enter new first name:"))
		acc.change_fname(str_1)
		print("Changed.")
	elif(x==2):
		str_1 = str(input("Enter new last name:"))
		acc.change_lname(str_1)
		print("Changed.")
	elif(x==3):
		to_dep = float(input("Enter amount to deposit."))
		acc.deposit(to_dep)
		print("Amount added.")
	elif(x==4):
		to_withdraw = float(input("Enter amount to withdraw."))
		acc.withdraw(to_withdraw)
		print("Operation finished.")
	elif(x==5):
		acc.deposit_interest()
	elif(x==6):
		id = input("Enter confirmation code:")
		acc.find_transaction(id)
	elif(x==7):
		acc.show_transactions()
	elif(x==8):
		acc.show_account()
	elif(x==9):
		print("Exiting.")
		break
