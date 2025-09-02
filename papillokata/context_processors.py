from chart.models import Chart, ChartItem
from accounts.models import CustomUser


def header_context(request):
	context = {}

	if request.user.is_authenticated:
		try:
			user = CustomUser.objects.get(username=request.user)
			chart = Chart.objects.filter(user=request.user).first()
			chartCount = ChartItem.objects.filter(chart=chart)

		except CustomUser.DoesNotExist:
			user = None
			chart = 0

		context.update({
			'USER':user,
			'CHART':chart,
		}) 

	return context

