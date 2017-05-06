from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
# Create your views here.
from estateTrade.models import estateTrade as etdb
from copy import deepcopy
import datetime

district_list= ['青秀区','江南区','兴宁区','良庆区','邕宁区','西乡塘区']

def et_index(request):
	context = {}
	result ={}
	for d in district_list:
		district_dict = {}
		# raise Exception(type(etdb.objects.filter(district=d).aggregate(Sum('acreage_amount'))))
		district_dict['acreage_amount'] = etdb.objects.filter(district=d).aggregate(Sum('acreage_amount'))['acreage_amount__sum']
		district_dict['apartment_amount'] = etdb.objects.filter(district=d).aggregate(Sum('apartment_amount'))['apartment_amount__sum']
		result[d] = deepcopy(district_dict)
	context['result'] = result
	return render(request, 'estate_trade/estate_trade_index.html', context)

def et_trend(request):
	context = {}
	context['error_msg'] = ''
	context['date_list'] = []
	context['acreage_amount_data_list'] = []
	context['apartment_amount_data_list'] = []
	try:
		district = request.GET.get('q')
	except Exception as e:
		context['error_msg'] = False
		district = "未指定"
	else:
		query_result = etdb.objects.filter(district=district).order_by('-trade_date')
		for i in query_result:
			context['date_list'].append(i.trade_date.strftime('%Y-%m-%d'))
			context['acreage_amount_data_list'].append(i.acreage_amount)
			context['apartment_amount_data_list'].append(i.apartment_amount)
	context['district'] = district
	return render(request, 'estate_trade/estate_trade_trend.html', context)

def et_trend_compare(request):
	context = {}
	context['error_msg'] = ''
	context['date_list'] = []
	context['acreage_amount_data_list'] = []
	context['data_dict'] = {}
	context['apartment_amount_data_list'] = []
	# query data from last 30 days
	boundary_date = datetime.date.today() - datetime.timedelta(days=30)
	query_result = etdb.objects.filter(trade_date__gte=boundary_date).order_by('-trade_date')
	date_list = query_result.distinct().values_list('trade_date', flat=True)
	context['date_list'] = [x.strftime('%Y-%m-%d') for x in date_list]
	for d in district_list:
		context['data_dict'][d] = query_result.filter(district=d).values_list('acreage_amount', flat=True)
	return render(request, 'estate_trade/estate_trade_compare.html', context)