from django.shortcuts import render
import requests
import json
import logging
from django.shortcuts import render, HttpResponse
import json
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':
        train_no = request.POST.get('train_no', '')
        
        if train_no:
            api_url = f'https://indian-railway-api.cyclic.app/trains/getTrain/?trainNo={train_no}'
            
            try:
                response = requests.get(api_url)
                
                logger.info(f'Response status code: {response.status_code}')
                logger.info(f'Response text: {response.text}')
                
                if response.status_code == 200:
                    data = response.json()['data']
                    train_data = {
                        'train_name': data.get('train_name', ''),
                        'from_stn_name': data.get('from_stn_name', ''),
                        'to_stn_name': data.get('to_stn_name', ''),
                        'from_time': data.get('from_time', ''),
                        'to_time': data.get('to_time', ''),
                        'average_speed': data.get('average_speed', '')
                    }
                    return render(request, 'index.html', {'train_data': train_data})
                else:
                    error_message = 'Failed to fetch train data.'
                    return render(request, 'index.html', {'error_message': error_message})
                
            except Exception as e:
                logger.error(f'Error fetching train data: {e}')
                error_message = 'Error fetching train data.'
                return render(request, 'index.html', {'error_message': error_message})

    return render(request, 'index.html')


def book_ticket(request):
    if request.method == 'POST':
        # Extract user input
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        age = request.POST.get('age', '')
        berth = request.POST.get('berth', '')

        # Train data from previous view
        train_data = request.POST.get('train_data', '')
        train_data = json.loads(train_data.replace("'", "\""))
        
        # Generate ticket content
        ticket_content = render_to_string('ticket.txt', {
            'train_name': train_data['train_name'],
            'from_stn_name': train_data['from_stn_name'],
            'to_stn_name': train_data['to_stn_name'],
            'from_time': train_data['from_time'],
            'to_time': train_data['to_time'],
            'average_speed': train_data['average_speed'],
            'name': name,
            'email': email,
            'age': age,
            'berth': berth
        })
        
        # Create and send the ticket as a text file
        response = HttpResponse(ticket_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=ticket_{name}.txt'
        return response
    
    return render(request, 'index.html')