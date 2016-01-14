from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r


class SubscribeNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """GET / must return code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_crsf(self):
        """HTML must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribeNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Leandro Garcia', cpf='12345678901', email='leandro.garcias@gmail.com', phone='19 991680300')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribeNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Ïnvalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Leandro Garcia', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')


'''
@unittest.skip('To be removed')
class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Leandro Garcia', cpf='12345678901',
                    email='leandro.garcias@gmail.com', phone='19 991680300')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
'''
