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
		if(balance>0):
			self.balance = balance
		else:
			print ("Balance cannot be negative")

	def change_fname(self,to_change):
		self.first_name = to_change

	def change_lname(self,to_change):
		self.last_name = to_change

	def deposit(self,to_add):
		self.balance += to_add
		self.transactions.append(Transaction(amount = to_add, account_number = self.account_number, operation_type = OperationType.Deposit, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))

	def withdraw(self,to_sub):
		if(self.balance-to_sub<0):
			self.transactions.append(Transaction(amount = to_sub, account_number = self.account_number, operation_type = OperationType.Operation_denied, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))
			print ("Transaction declined.")
		else:
			self.balance -= to_sub
			self.transactions.append(Transaction(amount = to_sub, account_number = self.account_number, operation_type = OperationType.Withdrawal, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))


	def deposit_interest(self):
		self.balance += self.balance*0.04
		self.transactions.append(Transaction(amount = self.balance*0.04, account_number = self.account_number, operation_type = OperationType.Interest_deposit, time_utc = datetime.utcnow(),tz_offset=self.tz_offset))


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
		print(("\n\nAccount ID -> {}\nAccount holder name -> {}\nBalance -> {}\nTime offset -> {}\n\n").format(str(self.account_number),str(self.first_name+" "+self.last_name),str(self.balance),str(self.tz_offset)))

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
		return time+timedelta(hours=tz_offset)





tz_offset = -5.5 #this is in hours
account = Account("123-421-213-231","Nirbhay","Narang",tz_offset,1000)
account.show_account()
account.deposit(1000)
account.deposit_interest()
account.withdraw(10000) #will fail
account.show_transactions()
account.change_fname("Info")
account.change_lname("Objects")
#you can call account.find_transaction on the confirmation code
account.show_account()
