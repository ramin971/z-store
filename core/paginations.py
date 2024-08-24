from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        return request.query_params.get('page_size',2)
    
    # def get_paginated_response_schema(self, schema):
    #     response =super().get_paginated_response_schema(schema)
    #     response.data['page_size']= self.request.query_params.get('page_size',2)
    #     return response

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['page_size'] = self.request.query_params.get('page_size',2)
        return response
   