from django.test import TestCase
from django.utils import timezone

from .models import Task


class TaskModelTests(TestCase):
    def test_create_task(self):
        t = Task.objects.create(title="Buy milk")
        self.assertIsNotNone(t.pk)
        self.assertEqual(t.title, "Buy milk")
        self.assertFalse(t.completed)

    def test_edit_task(self):
        t = Task.objects.create(title="Old")
        t.title = "New"
        t.description = "Updated"
        t.save()
        t.refresh_from_db()
        self.assertEqual(t.title, "New")
        self.assertEqual(t.description, "Updated")

    def test_delete_task(self):
        t = Task.objects.create(title="ToDelete")
        pk = t.pk
        t.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=pk)

    def test_mark_completed_and_toggle(self):
        t = Task.objects.create(title="Complete me")
        t.mark_completed()
        t.refresh_from_db()
        self.assertTrue(t.completed)
        t.mark_incomplete()
        t.refresh_from_db()
        self.assertFalse(t.completed)

    def test_due_date_and_is_overdue(self):
        past = timezone.now() - timezone.timedelta(days=2)
        future = timezone.now() + timezone.timedelta(days=2)

        t1 = Task.objects.create(title="Past", due_date=past)
        t2 = Task.objects.create(title="Future", due_date=future)
        t3 = Task.objects.create(title="NoDue")

        self.assertTrue(t1.is_overdue)
        self.assertFalse(t2.is_overdue)
        self.assertFalse(t3.is_overdue)

    def test_overdue_queryset(self):
        past = timezone.now() - timezone.timedelta(days=2)
        t1 = Task.objects.create(title="Past", due_date=past)
        # completed tasks should not be returned
        t1.mark_completed()
        t2 = Task.objects.create(title="Past2", due_date=past)

        overdue = Task.objects.overdue()
        self.assertIn(t2, overdue)
        self.assertNotIn(t1, overdue)
