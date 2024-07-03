from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import ItineraryMaster, ItineraryTemp
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from itineraries.serializers import ItineraryMasterSerializer, ItineraryDetailsSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.conf import settings



#<<----- Handle All the APIs Here ---->>


@api_view(["POST"])
def get_detail(request):
    if request.method == "POST":
        requestjson = json.loads(request.body)
        quotation_id = requestjson['quotation_id']
        if ItineraryTemp.objects.filter(quotation_id = quotation_id):
            itinerary = ItineraryTemp.objects.filter(quotation_id = quotation_id)
        
        # itineraryMaster1 = ItineraryMaster.objects.filter(itinerary_id = itineraryId)
        
            serializer = ItineraryDetailsSerializer(itinerary, many= True)

            return Response(serializer.data[0])
        else:
            return render(request, 'error_quotation_id.html')


@api_view(["GET", "POST"])
def getQuotationId(request):
    if request.method == "POST":
        requestjson = json.loads(request.body)
        quotation_id = requestjson['quotation_id']
        company_id = requestjson["company_id"]

        url = reverse('create-itinerary')
        redirect_url = f"{url}?quotation_id={quotation_id}&company_id={company_id}"
        
        return HttpResponseRedirect(redirect_url)
    else:
        return JsonResponse({'error': 'GET method not supported'}, status=400)

@api_view(["GET", "POST"])
def api_edit_itineraryDetails(request):
    quotation_id = 510
    itinerary = ItineraryTemp.objects.filter(quotation_id = quotation_id)
    
    # itineraryMaster1 = ItineraryMaster.objects.filter(itinerary_id = itineraryId)
    
    serializer = ItineraryDetailsSerializer(itinerary, many= True)
    dataJson = serializer.data
    print(dataJson)

    return Response(serializer.data[0])


@api_view(["POST"])
def delete_itinerary(request):
    if request.method == "POST":
        quotation_id = json.loads(request.body)["quotation_id"]
        itinerary = get_object_or_404(ItineraryTemp, quotation_id = quotation_id)
        itinerary.delete()







@api_view(["POST"])
def api_create(request):
    if request.method == "POST":
        requestJson = json.loads(request.body)

        #<----- Extract data from Json and Add to Database --------->
        if ItineraryTemp.objects.filter(quotation_id = requestJson[0]["quotation_id"]):
            return JsonResponse({
                "error":"quotationId already exist"
            })

        for data in requestJson:
    
            travel_destination = data["travel_destination"]
            created_at = data["created_at"]
            duration = data["duration"]
            lead_id = data["lead_id"]
            quotation_id = data["quotation_id"]

            

            # Create ItineraryTemp
            new_itinerary = ItineraryTemp(
                travel_destination=travel_destination,
                created_at = created_at,
                quotation_id=quotation_id,
                lead_id=lead_id,
                duration=duration
            )
            new_itinerary.save()
        
        itinerary = get_object_or_404(ItineraryTemp, quotation_id = quotation_id)
        itinerary_id = itinerary.itinerary_id

    

        for detail in data["details"]:

            title = detail["title"]
            day_number = detail["day_number"]
            activity = detail["activity"]
            
            itinerarydetails = ItineraryMaster(
                itinerary = itinerary,
                title = title,
                day_number = day_number,
                activity = activity
            )
            itinerarydetails.save()
        return JsonResponse({
            "success":"data insert successfully"
        })
    




#<<---- Handle All the Function Logic Here ---->>

@csrf_exempt
def search_itineraries(request, search=None):
    query = request.POST.get('query')
    itineraries = []

    if query:
        # Perform search query in the database
        if ItineraryTemp.objects.filter(travel_destination=query):
            itineraries = ItineraryTemp.objects.filter(travel_destination=query)
            print(itineraries)
        else:
            return render(request, 'error.html')
        
    else:
        itineraries = ItineraryTemp.objects.filter(travel_destination=search)
        print(itineraries)

    return render(request, 'itinerary_search.html', {'itineraries': itineraries})
        
@csrf_exempt
def create_itinerary(request, itinerary=None):
    if request.method == "POST":

        # response =  requests.get(url="api url")
        
        action = request.POST.get("action")
        
        
        # Check which button was pressed and handle accordingly
        if action == "create":

            quotation_id = request.POST.get("quotation_id")
            lead_id = request.POST.get("lead_id")
        
            print(quotation_id)

            # Handle itinerary creation logic
            travel_destination = request.POST.get("travel_destination")
            created_by = request.POST.get("created_by")
            # created_at_str = request.POST.get("created_at")
            duration_str = request.POST.get("duration")
            try:
                duration = int(duration_str)
            except ValueError:
                return HttpResponse("Invalid value for 'duration'", status=400)
                        
            # Prepare context for the Itinerary Details form
            range_list = range(1, duration + 1)
            context = {
                'range_list': range_list,               
                'travel_destination': travel_destination,
                'quotation_id': quotation_id,
                'duration': duration,
                'lead_id' : lead_id
 
            }
            # print(context["itinerary"].itinerary_id)
            # Redirect to create itinerary details page with context
            return render(request, 'create_itinerary.html', context)
        
        elif action == "save_details":
            
             # Handle saving itinerary details
            # itinerary_id = request.POST.get("itinerary_id")
            quotation_id = request.POST.get("quotation_id")
            lead_id = request.POST.get("lead_id")
        
            print(quotation_id)
            print(lead_id)

            # Extract quotation_id and company_id from query parameters
            

            # Handle itinerary creation logic
            travel_destination = request.POST.get("travel_destination")
            created_by = request.POST.get("created_by")
            # created_at_str = request.POST.get("created_at")
            duration_str = request.POST.get("duration")
            try:
                duration = int(duration_str)
            except ValueError:
                return HttpResponse("Invalid value for 'duration'", status=400)
            
            # Create ItineraryMaster
            itinerary = ItineraryTemp(
                travel_destination=travel_destination,
                quotation_id = quotation_id,
                lead_id = lead_id,
                
                # created_at=created_at,
                duration=duration
            )
            itinerary.save()



            try:
                itinerary = ItineraryTemp.objects.get(itinerary_id=itinerary.itinerary_id   )
            except ItineraryTemp.DoesNotExist:
                return HttpResponse("Invalid itinerary_id", status=404)
            
            duration = itinerary.duration

            for i in range(1, int(duration) + 1):
                day_number = request.POST.get(f'day_number_{i}')
                title = request.POST.get(f'title_{i}')
                activity_description = request.POST.get(f'activity_description_{i}')

                itinerary_detail = ItineraryMaster(
                    itinerary=itinerary,
                    day_number=day_number,
                    title=title,
                    activity=activity_description,
                )
                itinerary_detail.save()

            # Redirect to another view, or back to create_itinerary if you want to add more itineraries
            return redirect('itinerary_list')  # Change to the desired redirect URL


    return render(request, 'create_itinerary.html')

def create_or_edit_itinerary(request, itinerary_id=None):
    itinerary1 = get_object_or_404(ItineraryTemp, itinerary_id=itinerary_id)
    itinerary2 = ItineraryMaster.objects.filter(itinerary_id=itinerary1.itinerary_id)
    action = request.POST.get("action")

    duration = int(request.POST.get("duration", itinerary1.duration))
    range_list = range(1, duration + 1)

    if request.method == "POST":
        
        #Logic of add_day but handled with javascript
        # if action == "add_day":
        #     duration += 1
        #     range_list = range(1, duration + 1)

            
        
        quotation_id = request.GET.get("quotation_id")
        company_id = request.GET.get("company_id")

        print(duration)

        # Create ItineraryTemp
        new_itinerary = ItineraryTemp(
            travel_destination=itinerary1.travel_destination,
            created_by="",  # You should replace this with the actual user or creator
            quotation_id=quotation_id,
            company_id=company_id,
            duration=duration
        )
        new_itinerary.save()

        # Create ItineraryMaster entries
        for i in range(1, duration + 1):
            day_number = request.POST.get(f'day_number_{i}')
            title = request.POST.get(f'title_{i}')
            activity_description = request.POST.get(f'activity_description_{i}')

            itinerary_detail = ItineraryMaster(
                itinerary=new_itinerary,
                day_number=day_number,
                title=title,
                activity=activity_description,
                is_master=False
            )
            itinerary_detail.save()

        # Redirect to avoid form resubmission issues
        return redirect('itinerary_list')  # Replace 'success_url' with your actual URL name

    context = {
        "itineraries": itinerary2,
        "range_list": range_list,
        "itinerary": itinerary1,
        "duration": duration,
        
    }

    return render(request, 'create_customize.html', context)

def itinerary_list(request):
    itineraries = ItineraryTemp.objects.all() #fetch all itineraries
    return render(request, "itinerary_list.html", {'itineraries': itineraries})

def delete_itinerary(request, id):
    itinerary = get_object_or_404(ItineraryTemp, itinerary_id= id)

    # print(itinerary)
    if request.method == "POST":
        itinerary.delete()

        return JsonResponse({'success': True})  # Return JSON response
    return render(request, 'delete_itinerary.html', {'itinerary': itinerary})

def update_itinerary(request, id):
    itinerary = get_object_or_404(ItineraryTemp, itinerary_id = id)
    
    # print(itinerary)
    if request.method == "POST":
        itinerary.travel_destination = request.POST.get("travel_destination")
        # itinerary.created_at = request.POST.get("created_at")
        # itinerary.created_by =  request.POST.get("created_by")
        itinerary.duration = request.POST.get("duration")
        itinerary.save()

        return redirect("itinerary_list")
    return render(request, 'update_itinerary.html', {'itinerary':itinerary})

def create_itinerary_details(request, itinerary_id):
    if request.method == 'POST':  # Check if it's a POST request
        day_number = request.POST.get('day_number')  # Get form data
        # print(day_number)
        activity_description = request.POST.get('activity_description')
        # print(activity_description)
        title = request.POST.get('title')
        # print(title)

        # Create a new ItineraryDetails object
        itinerary_details = ItineraryMaster(
            itinerary_id=itinerary_id,  # Link to the master itinerary
            day_number=day_number,
            activity=activity_description,
            title = title
        )
        
        itinerary_details.save()  # Save to the database
        
        return redirect('itinerary_list')  # Redirect after successful creation
    
    # If not POST, render the form with the itinerary_id as context
    return render(request, 'create_itinerary_details.html', {'itinerary_id': itinerary_id})

def itinerary_with_details(request, itinerary_id):
    itinerary = get_object_or_404(ItineraryTemp, itinerary_id=itinerary_id)  # Fetch the specific itinerary
    # print(itinerary)
    details = ItineraryMaster.objects.filter(itinerary = itinerary) # Fetch related details
    # print(details)
    return render(request, 'itinerary_with_details.html', {'itinerary': itinerary, 'details': details})

def edit_itinerary_detail(request, detail_id):
    itinerary = get_object_or_404(ItineraryMaster, detail_id = detail_id)
    # print(itinerary)
    if request.method == 'POST':  # Check if it's a POST request
        itinerary.title = request.POST.get("title")
        itinerary.activity = request.POST.get("activity")
        
        itinerary.save()
        
        return redirect(reverse('itinerary_with_details', args=[itinerary.itinerary_id]))  # Redirect after successful creation
    return render(request, 'edit_itinerary_details.html', {'itinerary': itinerary})

def update_itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(ItineraryTemp, itinerary_id = itinerary_id)
    updated_duration = int(itinerary.duration) + 1
    print(itinerary.duration)
    if request.method == 'POST':  # Check if it's a POST request

        # Create a new ItineraryDetails object
        itinerary_details = ItineraryMaster(
            itinerary_id=itinerary_id,  # Link to the master itinerary
            day_number=request.POST.get('day_number'),
            activity=request.POST.get('activity'),
            title = request.POST.get('title'),
            is_master = False
        )
        
        itinerary_details.save()  # Save to the database

        itinerary.duration = str(updated_duration)
        itinerary.save()
        
         # Save to the database
               
        return redirect(reverse('itinerary_with_details', args=[itinerary.itinerary_id]))  # Redirect after successful creation
    return render(request, 'update_itinerary_details.html', {'itinerary': itinerary, "duration": str(updated_duration)})

def delete_itinerary_detail(request, detail_id):
    itinerary = get_object_or_404(ItineraryMaster, detail_id = detail_id)
    itinerary_duration = get_object_or_404(ItineraryTemp, itinerary_id = itinerary.itinerary_id)
    # print(itinerary)
    if request.method == "POST":
        if itinerary.is_master == "False":
            itinerary.delete()  #Delete the selected itinerary
            itinerary_duration.duration = int(itinerary_duration.duration) - 1
            itinerary_duration.save()
        elif itinerary.is_master == "True":
            return HttpResponse("You are Not Authorized")

        return redirect(reverse('itinerary_with_details', args=[itinerary.itinerary_id]))
    return render(request, 'delete_itinerary_details.html')





        
    



