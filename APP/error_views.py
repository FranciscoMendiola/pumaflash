from django.shortcuts import render

def render_error_page(request, titulo, subtitulo, mensaje, status):
    return render(request, "error/error.html", {
        "titulo": titulo,
        "subtitulo": subtitulo,
        "mensaje": mensaje,
    }, status=status)

def error_400_view(request, exception):
    return render_error_page(request, "Solicitud incorrecta", "Error 400", str(exception), 400)

def error_403_view(request, exception):
    return render_error_page(request, "Acceso denegado", "Error 403", str(exception), 403)

def error_404_view(request, exception):
    return render_error_page(request, "Página no encontrada", "Error 404", str(exception), 404)

def error_500_view(request):
    return render_error_page(request, "Error del servidor", "Error 500", "Ha ocurrido un error inesperado.", 500)
