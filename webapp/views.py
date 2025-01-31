from django.shortcuts import render,redirect

from .forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .utils import recommend, predictionPrice, metadata

from django.http import JsonResponse, HttpResponse

import plotly.graph_objects as go


from .models import QuestionnaireSubmission
# Create your views here.

# home page 
def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, 'webapp/index.html')


# Register a user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            
            return redirect('my-login')

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)



# Login a user

def my_login(request):
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data = request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password = password)
         
            if user is not None:
                auth.login(request, user)

                return redirect('user-agreement')

            
            
    context = {'form2':form}

    return render(request, 'webapp/my-login.html', context=context)




# user - logout

def user_logout(request):

    request.session['has_agreed_to_terms'] = False

    auth.logout(request)

    return redirect("my-login")


# # Agreement page

@login_required
def user_agreement(request):
    if request.method == 'POST':
        if 'agree' in request.POST:
            request.session['has_agreed_to_terms'] = True
            return redirect('dashboard')
    return render(request, 'webapp/user-agreement.html')




@login_required
def dashboard(request):
    username = request.user.first_name or request.user.username
    return render(request, 'webapp/dashboard.html', {'username':username})

@login_required
def questionnaire(request):
    if request.method == "POST":
        user_investment = request.POST.get('investment_amount')
        user_risk_preference = request.POST.get('risk_appetite')
        user_return_preference = request.POST.get('investment_preference')
        user_market_cap_preference = request.POST.get('market_cap')
        user_time_tolerance = request.POST.get('investment_duration')

        recommendations = recommend(user_investment, user_risk_preference,
            user_return_preference, user_market_cap_preference, user_time_tolerance)
        # print(recommendations)
        recommended_stocks = []
        for stock in recommendations:
            recommended_stocks.append(stock["Symbol"])
        try:

            submission = QuestionnaireSubmission(
                user=request.user if request.user.is_authenticated else None,  # Link to user if logged in
                market_cap=user_market_cap_preference,
                investment_amount=user_investment,
                investment_preference=user_return_preference,
                risk_appetite=user_risk_preference,
                investment_duration=user_time_tolerance,
            )
            submission.set_recommendations(recommended_stocks)
            # submission.set_distances(distances)
            submission.save()
        except:
            print("error at db")
        # print(user_investment)
        

        

        # print(type(recommendations))
        # to put in render below: 
        return render(request, 'webapp/recommendation.html', {'stocks': recommendations, 'submission_id': submission.id})
    
    return render(request, 'webapp/questionnaire.html')


@login_required
def recommendation(request):
    pass

@login_required
def prediction(request, symbol):
    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
    try:
        # Fetch the submission by ID
        submission = QuestionnaireSubmission.objects.get(id=submission_id)

        # Update the clicked stock field
        submission.clicked_stock = symbol
        submission.save()
    except:
        print("error while submitting clicked_stock")

    fig, stock_symbol, summary = predictionPrice(symbol)

    graph_html = fig.to_html(full_html = False)

    meta = metadata(symbol)

    return render (request, 'webapp/prediction.html', {'graph_html':graph_html, 'stock_symbol':stock_symbol, 'stock':meta, 'summary':summary})