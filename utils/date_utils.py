from datetime import datetime, timedelta

def get_week_start_end(date_obj):
    """
    Calcula o início (segunda-feira 00:00:00) e o fim (sexta-feira 23:59:59)
    da semana de trabalho para uma dada data.
    """
    # Garante que a data seja um objeto datetime
    if not isinstance(date_obj, datetime):
        date_obj = datetime(date_obj.year, date_obj.month, date_obj.day)

    # 0 = Segunda-feira, 6 = Domingo
    day_of_week = date_obj.weekday()

    # Calcula a segunda-feira da semana
    start_of_week = date_obj - timedelta(days=day_of_week)
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcula a sexta-feira da semana
    end_of_week = start_of_week + timedelta(days=4) # Segunda + 4 dias = Sexta
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

    return start_of_week, end_of_week