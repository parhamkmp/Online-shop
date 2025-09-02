from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'root/home.html'


class AboutPageView(TemplateView):
    template_name = 'root/about.html'

class CallUsView(TemplateView):
    template_name = 'root/call_us.html'


class Test404View(TemplateView):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response



class Test500View(TemplateView):
    template_name = '500.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 500
        return response



class Test403View(TemplateView):
    template_name = '403.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request,*args, **kwargs)
        response.status_code = 403
        return response

