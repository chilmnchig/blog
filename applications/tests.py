from django.test import TestCase
from django.urls import reverse

from .models import MontyHole
from .views.monty_hole import monty_open


class TestMontyHole(TestCase):
    def _getTarget(self):
        return reverse('index')

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertFalse(res.context['restart'])
        self.assertTemplateUsed(res, 'monty_hole/index.html')

    def test_post_select(self):
        nums = [1, 2, 3]
        res = self.client.post(
            self._getTarget(),
            data={
                'select': '1',
            }
        )
        self.assertEqual(res.context['nums'], {1, 2, 3})
        self.assertEqual(res.context['res'], 1)
        self.assertIn(res.context['ans'], nums)
        nums.remove(res.context['ans'])
        self.assertIn(res.context['opened'], nums)

    def test_post_open(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'res': '1',
                'ans': '3',
                'opened': '2',
                'open': '3',
            }
        )
        url = "{}?res=1&ans=3&opened=2&open=3".format(reverse('result'))
        self.assertRedirects(res, url)


class TestMontyHoleResult(TestCase):
    def _getTarget(self):
        return reverse('result')

    def test_get_changed_true(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'res': '1',
                'ans': '3',
                'opened': '2',
                'open': '3',
            }
        )
        self.assertTrue(res.context['change'])
        self.assertTrue(res.context['judge'])
        self.assertTrue(res.context['restart'])
        self.assertTemplateUsed(res, 'monty_hole/index.html')

    def test_get_changed_false(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'res': '1',
                'ans': '1',
                'opened': '2',
                'open': '3',
            }
        )
        self.assertTrue(res.context['change'])
        self.assertFalse(res.context['judge'])
        self.assertTemplateUsed(res, 'monty_hole/index.html')

    def test_get_not_changed_true(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'res': '3',
                'ans': '3',
                'opened': '2',
                'open': '3',
            }
        )
        self.assertFalse(res.context['change'])
        self.assertTrue(res.context['judge'])
        self.assertTrue(res.context['restart'])
        self.assertTemplateUsed(res, 'monty_hole/index.html')

    def test_get_not_changed_false(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'res': '3',
                'ans': '1',
                'opened': '2',
                'open': '3',
            }
        )
        self.assertFalse(res.context['change'])
        self.assertFalse(res.context['judge'])
        self.assertTrue(res.context['restart'])
        self.assertTemplateUsed(res, 'monty_hole/index.html')

    def test_get_invalid(self):
        res = self.client.get(self._getTarget())
        self.assertRedirects(res, reverse('index'))


class TestMontyOpen(TestCase):
    def test_correspond(self):
        self.assertIn(monty_open(1, 1), [2, 3])

    def test_incorrespond(self):
        self.assertEqual(monty_open(1, 2), 3)


class TestShowPercentage(TestCase):
    def test_show_percentage(self):
        for i in range(75):
            MontyHole.objects.create(change=True, judge=True)
            MontyHole.objects.create(change=False, judge=False)
        for i in range(25):
            MontyHole.objects.create(change=True, judge=False)
            MontyHole.objects.create(change=False, judge=True)
        self.assertEqual((75, 25), MontyHole.show_percentage())

    def test_zero_objects(self):
        self.assertEqual((0, 0), MontyHole.show_percentage())
