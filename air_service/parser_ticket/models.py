from django.db import models

class Ticket(models.Model):
    full_name = models.CharField("ФИО", max_length=200, blank=True)
    flight_number = models.CharField("Рейс", max_length=10, blank=True)
    departure_city = models.CharField("Город вылета", max_length=100, blank=True)
    arrival_city = models.CharField("Город прилёта", max_length=100, blank=True)
    departure_date = models.CharField("Дата вылета", max_length=20, blank=True)
    departure_time = models.CharField("Время вылета", max_length=10, blank=True)
    seat = models.CharField("Место", max_length=10, blank=True)
    ticket_class = models.CharField("Класс", max_length=20, blank=True)
    document_type = models.CharField("Тип документа", max_length=10)
    uploaded_file = models.FileField("Файл", upload_to="parser_ticket/")
    extracted_text = models.TextField("Извлеченный текст", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.flight_number}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"