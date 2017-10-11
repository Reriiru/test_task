from django.test import TestCase, RequestFactory
from pipeline_task.proxy_view import ProxyView


class ProxyTestCase(TestCase):
    request_factory = RequestFactory()

    def test_get(self):
        name = 'proxy'
        request = self.request_factory.get('/company/lanit/blog/339712/')
        view = ProxyView.as_view()

        response = view(request, name=name)

        self.assertEqual(response.status_code, 200)

        # self.assertEqual(context['name'], name)

    def test_post(self):
        name = 'proxy'
        request = self.request_factory.post('/company/lanit/blog/339712/')
        view = ProxyView.as_view()

        response = view(request, name=name)

        self.assertEqual(response.status_code, 200)
    
    def test_404(self):
        name = 'proxy'
        request = self.request_factory.get('/asdasdasd/asdasdasdasdasd')
        view = ProxyView.as_view()

        response = view(request, name=name)

        self.assertEqual(response.status_code, 404)

        # self.assertEqual(context['name'], name)
