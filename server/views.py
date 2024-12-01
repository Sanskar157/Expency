from django.shortcuts import render
import csv
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
import csv

# Create your views here.
def index(request):
  return render(request,'index.html')
 
@csrf_exempt  
def upload_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                # Print each row for debugging
                print(row)
                Transaction.objects.create(
                    amount=row['amount'],
                    date=row['date'],
                    description=row['description']
                )

            # Return a success message after processing the CSV
            return JsonResponse({'message': 'CSV file uploaded successfully'})

        except Exception as e:
            # Return error message if something goes wrong
            return JsonResponse({'error': str(e)}, status=500)
    
    return HttpResponse(status=400)




def get_monthly_spending(request):
    monthly_spending = (
        Transaction.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(amount=Sum('amount'))
        .order_by('month')
    )
    
    result = [
        {"month": month.strftime("%B"), "amount": amount}
        for month, amount in monthly_spending.values_list('month', 'amount')
    ]
    
    return JsonResponse(result, safe=False)