from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, time


def index(request):
    return render(request, 'index.html')

def health_check(request):
    health_check_1()
    #health_check_2()

def health_check_1(request):
    return JsonResponse({'message': 'OK'}, status=200)

def health_check_2(request):
    # Define el rango horario permitido
    hora_inicio = time(7, 0)  # 7:00 AM
    hora_fin = time(17, 0)    # 15:00 PM
    hora_actual = datetime.now().time()

    if hora_inicio <= hora_actual <= hora_fin:
        return JsonResponse({'message': 'OK'}, status=200)
    else:
        return JsonResponse({'error': 'Servicio fuera de horario permitido'}, status=403)
