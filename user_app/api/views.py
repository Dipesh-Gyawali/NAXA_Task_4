from django.http import JsonResponse
from .models import Project, Municipality

def project_count_by_municipality(request):
    # Get filters from request parameters
    province = request.GET.get('province')
    district = request.GET.get('district')

    # Construct queryset based on filters
    qs = Project.objects.all()

    if province:
        qs = qs.filter(municipality__district__province__name=province)

    if district:
        qs = qs.filter(municipality__district__name=district)

    # Group projects by municipality and calculate count and budget
    qs = qs.values('municipality__id', 'municipality__name').annotate(
        count=Count('id'),
        budget=Sum('budget')
    )

    # Build the response data
    response_data = []

    for item in qs:
        response_data.append({
            'id': item['municipality__id'],
            'name': item['municipality__name'],
            'count': item['count'],
            'budget': item['budget']
        })

    return JsonResponse(response_data, safe=False)
