from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import calendar
from datetime import datetime, timedelta, date

# pages = Blueprint("pages", __name__)
from app import app

# set fares
default_monthlyfare = 100
default_tenpassfare = "{:.2f}".format(27.75)
default_dailyfare = "{:.2f}".format(3.50)
default_holidays = 0
currentmonth = date.today().month
currentyear = date.today().year


@app.route("/")
def home():
    return render_template("index.html",  monthlyfare=default_monthlyfare, tenpassfare=default_tenpassfare, dailyfare=default_dailyfare, holidays=default_holidays, currentyear=currentyear, currentmonth=currentmonth, resultdiv="blockhidden")


# Main Search routine using home page
@app.route("/", methods=['GET', 'POST'])
def echo():
    # get index form data

    if request.method == "POST":

        # get form  data
        monthlyfare = request.form["monthlyfare"]
        tenpassfare = request.form["tenpassfare"]
        dailyfare = request.form["dailyfare"]
        holidays = request.form["holidays"]
        currentyearmonth = request.form["currentyearmonth"]

        # SET DEFAULTS
        # input monthly fare
        if monthlyfare == '':
            monthlyfare = default_monthlyfare
        else:
            monthlyfare = monthlyfare

        # input ten pass fare
        if tenpassfare == '':
            tenpassfare = float(default_tenpassfare)
        else:
            tenpassfare = float(tenpassfare)

        # input daily fare
        if dailyfare == '':
            dailyfare = float(default_dailyfare)
        else:
            dailyfare = float(dailyfare)

        # input holidays
        if holidays == '':
            holidays = default_holidays
        else:
            holidays = int(holidays)

        # Get current dates-substitute today if no entry
        if currentyearmonth != "":
            selected_month = datetime.strptime(currentyearmonth, "%Y-%m")
        if currentyearmonth == '':
            currentyear = date.today().year
            currentmonth = date.today().month
        else:
            currentmonth = selected_month.month
            currentyear = selected_month.year

        currentmonthtext = calendar.month_name[currentmonth]

        # Count days in month
        daysinmonthcount = calendar.monthrange(currentyear, currentmonth)[1]

        # Function to count week days
        def workdays(d, end, excluded=(6, 7)):
            days = []
            while d.date() <= end.date():
                if d.isoweekday() not in excluded:
                    days.append(d)
                d += timedelta(days=1)
            return len(days)

        # execute function
        monthdays = (workdays(datetime(currentyear, currentmonth, 1),
                              datetime(currentyear, currentmonth, daysinmonthcount)))

        # set daily
        finaldaycount = monthdays - holidays
        monthlycostperday = monthlyfare/(finaldaycount)
        tenpasscostperday = (float(tenpassfare)/10)*2
        tenpasscostpermonth = tenpasscostperday * finaldaycount
        dailyperday = dailyfare * 2
        dailycostpermonth = dailyperday * finaldaycount

        daysinmonth = str(daysinmonthcount)
        travel_days = str(finaldaycount)
        monthlyfare = "${:.2f}".format(monthlyfare)
        monthly_perday = "${:.2f}".format(monthlycostperday)
        tenpassfare = "${:.2f}".format(tenpassfare)
        tenpass_perday = "${:.2f}".format(tenpasscostperday)
        tenpasscostpermonth = "${:.2f}".format(
            tenpasscostpermonth)
        dailyfare = "${:.2f}".format(dailyfare)
        daily_perday = "${:.2f}".format(dailyperday)
        dailycostpermonth = "${:.2f}".format(dailycostpermonth)

    return render_template('index.html',
                           currentyear=currentyear,
                           currentmonthtext=currentmonthtext,
                           daysinmonth=daysinmonth,
                           travel_days=travel_days,
                           c_monthlyfare=monthlyfare,
                           monthly_perday=monthly_perday, tenpasscostpermonth=tenpasscostpermonth,
                           c_tenpassfare=tenpassfare,
                           tenpass_perday=tenpass_perday,
                           c_dailyfare=dailyfare,
                           daily_perday=daily_perday,
                           dailycostpermonth=dailycostpermonth,
                           resultdiv="blockvisible")

    # result_title = "Calculations for " + \
    #     str(currentyear) + " " + currentmonthtext
    # daysinmonth = "Days in the month: " + \
    #     str(daysinmonthcount) + " days"
    # travel_days = "Bus travel days: " + str(finaldaycount) + " days"
    # monthlyfare = "Monthly: " + "${:.2f}".format(monthlyfare)
    # monthly_perday = "${:.2f}".format(monthlycostperday) + " per day"
    # tenpassfare = "10 pack: " + "${:.2f}".format(tenpassfare)
    # tenpass_perday = "${:.2f}".format(tenpasscostperday) + " per day"
    # tenpasscostpermonth = "${:.2f}".format(
    #     tenpasscostpermonth) + " per month"
    # dailyfare = "Single Use: " + "${:.2f}".format(dailyfare)
    # daily_perday = "${:.2f}".format(dailyperday) + " per day"
    # dailycostpermonth = "${:.2f}".format(dailycostpermonth) + " per month"

    # return render_template('index.html', result_title=result_title, daysinmonth=daysinmonth, travel_days=travel_days, c_monthlyfare=monthlyfare, monthly_perday=monthly_perday, tenpasscostpermonth=tenpasscostpermonth, c_tenpassfare=tenpassfare, tenpass_perday=tenpass_perday, c_dailyfare=dailyfare, daily_perday=daily_perday, dailycostpermonth=dailycostpermonth, resultdiv="blockvisible")
