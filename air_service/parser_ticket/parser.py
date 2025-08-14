import re
from datetime import datetime

# "Парсер для извлечения данных из билета Аэрофлота
def parse_aeroflot_ticket(text):
    data = {
        'full_name': '',
        'flight_number': '',
        'departure_city': '',
        'arrival_city': '',
        'departure_date': '',
        'departure_time': '',
        'seat': '',
        'ticket_class': '',
    }

    # Нормализуем текст для лучшего поиска
    text_upper = text.upper()
    text_lines = text.split('\n')
    
    # Поиск ФИО - несколько вариантов
    name_patterns = [
        r'(?:ПАССАЖИР|PASSENGER)[\s\n:]+([A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+)',
        r'(?:ФИО|FULL NAME)[\s\n:]+([A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+)',
        r'([A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+)',  # ФИО из 3 слов
        r'([A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+)',  # ФИО из 2 слов
    ]
    
    for pattern in name_patterns:
        passenger_match = re.search(pattern, text, re.IGNORECASE)
        if passenger_match:
            data['full_name'] = passenger_match.group(1).strip()
            break

    # Поиск номера рейса - несколько вариантов
    flight_patterns = [
        r'\b(SU\s*\d{3,4})\b',
        r'\b(АЭРОФЛОТ\s*SU\s*\d{3,4})\b',
        r'\b(РЕЙС|FLIGHT)[\s\n:]+(SU\s*\d{3,4})\b',
        r'\b(SU\d{3,4})\b',
    ]
    
    for pattern in flight_patterns:
        flight_match = re.search(pattern, text_upper)
        if flight_match:
            flight_num = flight_match.group(1) if len(flight_match.groups()) == 1 else flight_match.group(2)
            data['flight_number'] = flight_num.replace(' ', '')
            break

    # Cписок городов
    cities = {
        'MOW': 'Москва',
        'LED': 'Санкт-Петербург',
        'SVX': 'Екатеринбург',
        'AER': 'Сочи',
        'KRR': 'Краснодар',
        'ROV': 'Ростов-на-Дону',
        'UFA': 'Уфа',
        'KZN': 'Казань',
        'VOG': 'Волгоград',
        'GOJ': 'Нижний Новгород',
        'OMS': 'Омск',
        'TOF': 'Томск',
        'NJC': 'Нижневартовск',
        'SGC': 'Сургут',
        'KUF': 'Самара',
        'VVO': 'Владивосток',
        'KHV': 'Хабаровск',
        'IKT': 'Иркутск',
        'OVB': 'Новосибирск',
        'MMK': 'Мурманск',
        'ARH': 'Архангельск',
        'PEE': 'Пермь',
        'CEK': 'Челябинск',
        'TJM': 'Тюмень',
        'ASF': 'Астрахань',
        'STW': 'Ставрополь',
        'MCX': 'Махачкала',
        'GRV': 'Грозный',
        'NAL': 'Нальчик',
        'ESL': 'Элиста',
        'VOG': 'Волгоград',
        'SIP': 'Симферополь',
        'KGD': 'Калининград',
        'PEE': 'Пермь',
        'CEK': 'Челябинск',
        'TJM': 'Тюмень',
        'ASF': 'Астрахань',
        'STW': 'Ставрополь',
        'MCX': 'Махачкала',
        'GRV': 'Грозный',
        'NAL': 'Нальчик',
        'ESL': 'Элиста',
        'VOG': 'Волгоград',
        'SIP': 'Симферополь',
        'KGD': 'Калининград',
    }
    
    # Поиск маршрута
    city_codes = '|'.join(cities.keys())
    route_patterns = [
        rf'\b({city_codes})\s*[-—>]\s*({city_codes})\b',
        rf'\b({city_codes})\s*-\s*({city_codes})\b',
        rf'\b({city_codes})\s*→\s*({city_codes})\b',
        rf'\b({city_codes})\s+({city_codes})\b',
    ]
    
    for pattern in route_patterns:
        route_match = re.search(pattern, text_upper)
        if route_match:
            data['departure_city'] = cities.get(route_match.group(1), route_match.group(1))
            data['arrival_city'] = cities.get(route_match.group(2), route_match.group(2))
            break
    
    # Если не нашли маршрут, ищем отдельные коды городов
    if not data['departure_city'] or not data['arrival_city']:
        city_matches = re.findall(rf'\b({city_codes})\b', text_upper)
        if len(city_matches) >= 2:
            data['departure_city'] = cities.get(city_matches[0], city_matches[0])
            data['arrival_city'] = cities.get(city_matches[1], city_matches[1])

    # Поиск даты - несколько форматов
    date_patterns = [
        r'\b(\d{2}[A-Z]{3}\d{4})\b',  
        r'\b(\d{2}\.\d{2}\.\d{4})\b',  
        r'\b(\d{2}/\d{2}/\d{4})\b',    
        r'\b(\d{2}-\d{2}-\d{4})\b',    
        r'\b(\d{2}\s+[A-ZА-Я]{3,}\s+\d{4})\b',  
        r'\b(\d{1,2}\.\d{1,2}\.\d{2,4})\b',     
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, text, re.IGNORECASE)
        if date_match:
            data['departure_date'] = date_match.group(1)
            break

    # Поиск времени
    time_patterns = [
        r'\b(\d{1,2}:\d{2})\b',        
        r'\b(\d{1,2}:\d{2}:\d{2})\b',  
        r'\b(\d{1,2}\.\d{2})\b',       
        r'\b(\d{1,2}ч\s*\d{2}м)\b',    
    ]
    
    for pattern in time_patterns:
        time_match = re.search(pattern, text)
        if time_match:
            time_str = time_match.group(1)
            # Нормализация времени
            if '.' in time_str:
                time_str = time_str.replace('.', ':')
            elif 'ч' in time_str:
                time_str = re.sub(r'(\d+)ч\s*(\d+)м', r'\1:\2', time_str)
            data['departure_time'] = time_str
            break

    # Поиск места в самолете
    seat_patterns = [
        r'\b(\d{1,2}[A-Z])\b',         
        r'\b([A-Z]\d{1,2})\b',         
        r'\b(МЕСТО|SEAT)[\s\n:]+(\d{1,2}[A-Z])\b',
        r'\b(МЕСТО|SEAT)[\s\n:]+([A-Z]\d{1,2})\b',
    ]
    
    for pattern in seat_patterns:
        seat_match = re.search(pattern, text_upper)
        if seat_match:
            if len(seat_match.groups()) == 1:
                data['seat'] = seat_match.group(1)
            else:
                data['seat'] = seat_match.group(2)
            break

    # Поиск класса обслуживания
    class_patterns = [
        r'\b(ECONOM|ЭКОНОМ)\b',
        r'\b(BUSINESS|БИЗНЕС)\b',
        r'\b(PREMIUM|ПРЕМИУМ)\b',
        r'\b(FIRST|ПЕРВЫЙ)\b',
        r'\b(КЛАСС|CLASS)[\s\n:]+(ECONOM|BUSINESS|PREMIUM|FIRST)\b',
    ]
    
    class_mapping = {
        'ECONOM': 'Эконом',
        'ЭКОНОМ': 'Эконом',
        'BUSINESS': 'Бизнес',
        'БИЗНЕС': 'Бизнес',
        'PREMIUM': 'Премиум',
        'ПРЕМИУМ': 'Премиум',
        'FIRST': 'Первый',
        'ПЕРВЫЙ': 'Первый',
    }
    
    for pattern in class_patterns:
        class_match = re.search(pattern, text_upper)
        if class_match:
            cls = class_match.group(1) if len(class_match.groups()) == 1 else class_match.group(2)
            data['ticket_class'] = class_mapping.get(cls, cls)
            break

    # Дополнительная обработка: поиск по контексту
    if not data['full_name']:
        # Поиск строк, которые могут содержать ФИО
        for line in text_lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 50:
                # Проверяем, содержит ли строка русские буквы и выглядит как ФИО
                if re.search(r'[А-Яа-я]', line) and re.search(r'\s+', line):
                    words = line.split()
                    if len(words) >= 2 and all(len(word) > 1 for word in words[:2]):
                        data['full_name'] = ' '.join(words[:2])
                        break

    return data