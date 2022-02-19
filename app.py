from flask import Flask, request
import africastalking
import os
import variables
import re
import maya
from maya import MayaInterval
from datetime import datetime
from dateutil.parser import parse
import mysql.connector

app = Flask(__name__)

username = "sandbox"
api_key = "0f54c06969af94baa76c50efbcc1daaecb9b75f254d3388c85edfd9d21ff7ad0"
africastalking.initialize(username, api_key)

sms = africastalking.SMS

db = mysql.connector.connect(
    
    host = "137.184.54.169",
    user = "kaguius",
    passwd = "U6xZfLn9A7Swc%P9",
    database = "finabora",
    autocommit = True,
    port ="3306",
)
@app.route('/', methods=['POST', 'GET'])

def Greetings():
    

   
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    text_input= request.values.get("text")
    text = ''.join(text_input.split())

    if text == "":

        phone_number = ""
        phone_number = request.values.get("phoneNumber","default")
        variables.number = phone_number.split('+')[1] 
        print(variables.number)

        variables.now = maya.MayaDT.from_datetime(datetime.utcnow())
        Time_zone = variables.now.hour +3

        if 5<= Time_zone <12 :
            Good_Morning="Good Morning"
            variables.response =("CON {}"
                                        "\nHow may i help you"
                                        "\n  -Limit "
                                        "\n  -Balance"
                                        "\n  -Loan"
                                        "\n  -Amount"
            ).format(Good_Morning)

        elif  12 <= Time_zone < 17 :
            Good_Afternoon="Good Afternoon"
            variables.response =("CON {}"
                                        "\nHow may i help you"
                                        "\n  -Limit "
                                        "\n  -Balance"
                                        "\n  -Loan"
                                        "\n  -Amount"
                    ).format(Good_Afternoon)
        else:
            Good_Evening="Good Evening"
            variables.response =("CON {}"
                                        "\nHow may i help you"
                                        "\n  -Limit "
                                        "\n  -Balance"
                                        "\n  -Loan"
                                        "\n  -Amount"
                    ).format(Good_Evening)

        mycursor = db.cursor()
        mycursor.execute('''SELECT primary_phone FROM s_staff WHERE primary_phone = (%s)''', (variables.number,))
        variables.checkNumber = mycursor.fetchall()
        Balance()
    
    return variables.response

     
 
def Balance():

    text_input= request.values.get("text")
    text = ''.join(text_input.split())

    if (text == "balance" or text == "Balance" ):

        if (variables.number,) in variables.checkNumber:
            mycursor = db.cursor()
            mycursor.execute('''SELECT first_name FROM s_staff WHERE primary_phone = (%s)''', (variables.number,))
            name = mycursor.fetchone()
            namef = name[0]
            print(name)
            print(namef)
                
                

            now = datetime.now()
            Time_zone = now.hour +3
            date = Time_zone.strftime("%d/%m/%Y, %H:%M")

            variables.response=("END Dear {}, your effective balance as at {} is KES $loan_balance."
            ).format(namef,date)
            
        else:
                variables.response=("END Dear customer, we do not seem to have your details on file. Please visit the office to get registered.")
        
    

    
        
    return variables.response
    


    


    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
