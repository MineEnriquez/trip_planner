from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.utils.dateparse import parse_date
from .models import User, Trips
# line added during the implementation of validation .
from django.contrib import messages
import bcrypt


def index(request):
    request.session.flush()
    if request.method == "GET":
        return render(request, "login_and_reg_app/index.html")

    if request.method == "POST":
        return render(request, "login_and_reg_app/index.html")

# On POST: Processing view- no rendering of html
# On GET: Render the html page


def register(request):
    if request.method == "GET":
        return render(request, "login_and_reg_app/index.html")

    elif request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
        else:
            # if passwords match:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt())  # create the hash
            print(pw_hash)
            us = User.objects.create(
                last_name=request.POST['last_name'], first_name=request.POST['first_name'], email=request.POST['email'], password_hash=pw_hash)
            # ----- MODIFY NEXT LINE TO REUSE -----
            request.session['current_user'] = us.email
            request.session['user'] = us.first_name
            request.session['user_id'] = us.id
            # never render on a post, always redirect!
            return redirect("/success")
        return redirect('/register')


def success(request):
    try:
        if request.session['current_user'] == "":
            return redirect('/')
        else:
            return redirect('/dashboard')
            # return render(request, "login_and_reg_app/success.html")
    except:
        return redirect('/')


def validate_login(request):
    request.session.flush()
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), user.password_hash.encode()):
                print("password match")
                request.session['current_user'] = user.email
                request.session['user'] = user.first_name
                request.session['user_id'] = user.id
                return redirect("/success")
            else:
                print("failed password")
                messages.error(request, "Wrong password was provided")
                return redirect('/register')
        except:
            print("user not found")
            messages.error(request, "Username not found")
            return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def dashboard_render(request):
    print("Dashboard - viewing trips:----")
    if 'user_id' in request.session:
        all_user_trips = Trips.objects.filter(
            user_id_id=request.session['user_id']).order_by("-id")
        all_other_trips = Trips.objects.exclude(
            user_id_id=request.session['user_id'])
    else:
        return redirect('/')

    context = {
        "all_user_trips": all_user_trips,
        "all_other_trips": all_other_trips
    }
    return render(request, "login_and_reg_app/dashboard.html", context)


def trip_create(request):
    if request.method == "GET":
        return redirect('/trips/new')
    if request.method == "POST":
        # Pass the post data to the mehod we wrote and save the response in a variable called errors
        errors = Trips.objects.basic_validator(request.POST)

        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            user = User.objects.get(id=request.session['user_id'])
            new_trip = Trips.objects.create(destination=request.POST['destination'],
                                            start_date=request.POST['start_date'],
                                            end_date=parse_date(
                                                request.POST['end_date']),
                                            plan=request.POST['plan'],
                                            user_id=user)
            print("-----------------")
            print(new_trip.destination)
            # newtrip = "/trips/" + str(new_trip.id)
            return redirect("/dashboard")


def trip_create_render(request):
    return render(request, "login_and_reg_app/create.html")


def trip_remove(request, trip_id):
    rem = Trips.objects.get(id=trip_id)
    print(f"deleting a record {str(trip_id)}")
    rem.delete()
    return redirect("/dashboard")


def trip_edit(request, trip_id):
    trip = Trips.objects.get(id=trip_id)
    print(trip.destination)
    context = {
        "trip_info": trip,
        "start_date": trip.start_date.strftime("%Y-%m-%d"),
        "end_date": trip.end_date.strftime("%Y-%m-%d")
    }
    return render(request, "login_and_reg_app/Update.html", context)


def view_trip(request, trip_id):
    trip = Trips.objects.get(id=trip_id)
    print(trip.destination)
    context = {
        "trip_info": trip
    }
    return render(request, "login_and_reg_app/trip.html", context)


def trip_update(request, trip_id):
    if request.method == "POST":
        # Pass the post data to the mehod we wrote and save the response in a variable called errors
        errors = Trips.objects.basic_validator(request.POST)

        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            trip = Trips.objects.get(id=trip_id)

            trip.destination = request.POST['destination']
            trip.start_date = parse_date(request.POST['start_date'])
            trip.end_date = parse_date(request.POST['end_date'])
            trip.plan = request.POST['plan']
            trip.save()

            print("-----------------")
            print(trip.destination)
            # newtrip = "/trips/" + str(new_trip.id)
            return redirect("/dashboard")

# "/trips/{{trip.id}}"


def trips_join(request, trip_id):
    us = User.objects.get(id=request.session['user_id'])
    tp = Trips.objects.get(trip_id)
    trip = Trips.objects.create(destination=tp.destination,
                                start_date=tp.start_date,
                                end_date=tp.end_date,
                                plan=tp.plan, user_id=us)
    print("-----------------")
    print(trip.destination)
    return redirect("/dashboard")
