from django.test import TestCase
from django.urls import reverse

from randomapp.weapon_names import weapon_names


class TestPerform(TestCase):
    def _getTarget(self):
        return reverse('perform')

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertEqual(res.context['result'], "-")
        self.assertFalse(res.context['error'])
        self.assertEqual(res.context['min'], 1)
        self.assertEqual(res.context['max'], 10)
        self.assertTemplateUsed(res, 'random/index.html')

    def test_get_display(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'display': '表示',
                'min': 1,
                'max': 10,
            }
        )
        self.assertIn(res.context['result'], range(1, 11))
        self.assertFalse(res.context['error'])
        self.assertEqual(res.context['min'], 1)
        self.assertEqual(res.context['max'], 10)
        self.assertTemplateUsed(res, 'random/index.html')

    def test_get_display_one(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'display': '表示',
                'min': 1,
                'max': 1,
            }
        )
        self.assertEqual(res.context['result'], 1)
        self.assertFalse(res.context['error'])
        self.assertEqual(res.context['min'], 1)
        self.assertEqual(res.context['max'], 1)
        self.assertTemplateUsed(res, 'random/index.html')

    def test_get_display_error(self):
        res = self.client.get(
            self._getTarget(),
            data={
                'display': '表示',
                'min': 13,
                'max': 1,
            }
        )
        self.assertEqual(res.context['result'], "正しく整数を入力してください")
        self.assertTrue(res.context['error'])
        self.assertTemplateUsed(res, 'random/index.html')


class TestWeapon(TestCase):
    def _getTarget(self):
        return reverse('weapon')

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertEqual(res.context['result'], "")
        self.assertTemplateUsed(res, 'random/weapon.html')

    def test_get_display(self):
        res = self.client.get(self._getTarget(), data={'display': '表示'})
        self.assertIn(res.context['result'], weapon_names)
        self.assertTemplateUsed(res, 'random/weapon.html')
