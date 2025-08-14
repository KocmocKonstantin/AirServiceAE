from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TicketUploadForm
from .models import Ticket
from .wrapper_ticket import extract_text_from_uploaded_file
from .parser import parse_aeroflot_ticket
import os

def upload_ticket(request):
    if request.method == 'POST':
        form = TicketUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save()

            # Определение типа файла
            filename = ticket.uploaded_file.name.lower()
            if filename.endswith('.pdf'):
                file_type = 'pdf'
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                file_type = 'image'
            else:
                messages.error(request, "Поддерживаются только PDF и изображения.")
                ticket.delete()
                return redirect('upload')

            try:
                # Извлечение текста
                file_path = ticket.uploaded_file.path
                raw_text = extract_text_from_uploaded_file(file_path, file_type)

                # Парсинг
                parsed_data = parse_aeroflot_ticket(raw_text)

                # Заполнение модели
                for key, value in parsed_data.items():
                    setattr(ticket, key, value)
                ticket.document_type = 'PDF' if file_type == 'pdf' else 'Image'
                ticket.extracted_text = raw_text  
                ticket.save()

                messages.success(request, "Билет успешно обработан")
                return redirect('parser_ticket:ticket_list')
            except Exception as e:
                # В случае ошибки удаляем билет и показываем сообщение
                ticket.delete()
                messages.error(request, f"Ошибка при обработке файла: {str(e)}")
                return redirect('parser_ticket:upload')
    else:
        form = TicketUploadForm()
    return render(request, 'parser_ticket/upload.html', {'form': form})

def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-uploaded_at')
    return render(request, 'parser_ticket/list.html', {'tickets': tickets})