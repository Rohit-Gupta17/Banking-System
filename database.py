import sqlite3
import random


def bank_table():
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("""create table if not exists customer_detail(
        customer_id integer primary key autoincrement,
        account_no text unique not null,
        name text not null,
        email text unique not null,
        mobile text unique not null,
        pin text not null,
        balance real default 0,
        create_at text)""")
    c.execute("""create table if not exists transaction_detail(
        transaction_id integer primary key autoincrement,
        account_no integer,
        transaction_type text,
        amount real,
        balance real,
        transaction_date timestamp default current_timestamp)""")
    
    conn.commit()
    conn.close()
    


def generated_acc():
    
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    while True:
        account_no=random.randint(1000000000,9999999999)
    
        c.execute("select account_no from customer_detail where account_no=?",(account_no,))
        
        result=c.fetchone()
        
        if result is None:
            conn.close()
            return account_no
        
def register_acc(name,email,mobile,pin,amount):
    
    if amount<500:
        return False , " minimum opening account balance ₹500"
    
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("select email from customer_detail where email=?",(email,))
    
    result=c.fetchone()
    
    if result is not None:
        conn.close()
        return False,"email already exist"
    
    account_no=generated_acc()
    
    c.execute("""insert into customer_detail(account_no,name,email,mobile,pin,balance)
              values(?,?,?,?,?,?)""",(account_no,name,email,mobile,pin,amount))
    
    c.execute("""insert into transaction_detail(account_no, transaction_type, amount, balance)
             values(?,?,?,?)""",(account_no,"Account opening",amount,amount))
    
    conn.commit()
    conn.close()
    return True, account_no


def customer_login(account_no,pin):
    
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("select * from customer_detail where account_no=? and pin=?",(account_no,pin))
    
    customers=c.fetchone()
    conn.close()
    
    return customers

def get_customer(account_no):
    
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("select * from customer_detail where account_no=?",(account_no,))
    
    customers=c.fetchone()
    c.close()
    
    return customers

def deposite(account_no,amount):
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("update customer_detail set balance=balance + ? where account_no=?",(amount,account_no))
    
    c.execute("select balance from customer_detail where account_no=?",(account_no,))
    
    balance=c.fetchone()[0]
    
    c.execute("insert into transaction_detail(account_no,transaction_type,amount,balance) values(?,?,?,?)",(account_no,"deposite",amount,balance))
    
    conn.commit()
    conn.close()
    
    return True

def withdraw(account_no,amount):

    conn = sqlite3.connect("banking.db")
    c = conn.cursor()

    c.execute(
        "select balance from customer_detail where account_no=?",
        (account_no,)
    )

    result = c.fetchone()

    if result is None:

        conn.close()

        return False, "Account not found"

    balance = result[0]

    if amount > balance:

        conn.close()

        return False, "Insufficient balance"

    # Withdraw

    c.execute(
        "update customer_detail set balance=balance-? where account_no=?",
        (amount,account_no)
    )

    # Get new balance

    c.execute(
        "select balance from customer_detail where account_no=?",
        (account_no,)
    )

    balance = c.fetchone()[0]

    # Save transaction

    c.execute("""
        insert into transaction_detail
        (account_no,transaction_type,amount,balance)
        values(?,?,?,?)
    """,(
        account_no,
        "Withdraw",
        amount,
        balance
    ))

    conn.commit()
    conn.close()

    return True, "Withdraw successful"

def transaction_history(account_no):
    conn=sqlite3.connect("banking.db")
    c=conn.cursor()
    
    c.execute("""select transaction_type,
              amount,
              balance,
              transaction_date from transaction_detail
              where account_no=? 
              order by transaction_id desc""",(account_no,))
    
    transactions=c.fetchall()
    conn.close()
    
    return transactions

def change_pin(account_no,old_pin,new_pin):

    conn = sqlite3.connect("banking.db")
    c = conn.cursor()

    c.execute(
        "select pin from customer_detail where account_no=?",
        (account_no,)
    )
    result = c.fetchone()

    if result is None:

        conn.close()

        return False

    pin = result[0]

    if pin == old_pin:

        c.execute(
            "update customer_detail set pin=? where account_no=?",
            (new_pin,account_no)
        )

        conn.commit()
        conn.close()

        return True

    conn.close()

    return False