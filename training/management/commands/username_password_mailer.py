from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
import csv

class Command(BaseCommand):

    def sendmail(self, information):
        # print information
        from_user = 'server@digitalgreen.org'
        to = information[3]
        print to
        subject = "Change of username and password"
        greeting = "Hi " + information[0] + "!!! \n"
        message = "Your Username and password has been changed for logging into our system. Please use the same for any future use.\n"
        new_credentials = "\nYour new credentials are : \n"
        new_username = "Username : " + information[1] + "\n"
        new_password = "Password : " + information[2] + "\n"
        thanks = "\nThanks you for your support!!! \nTech team \nsystem@digitalgreen.org"

        body = greeting + message + new_credentials + new_username + new_password + thanks
        try:
            msg = EmailMultiAlternatives(subject,body,from_user,[to])
            msg.send()
        except Exception as e:
            print e

    def handle(self,*args,**options):
        with open("training/management/commands/username_password.csv","rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                self.sendmail(row)
