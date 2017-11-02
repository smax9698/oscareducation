import random

from django.test import TestCase
from django.utils import timezone

from resources.models import Resource
from stats.models import ResourceStudent
from stats.StatsObject import ResourcesViewed
from users.models import User, Student


class RetrieveResourcesAccessedByStudent(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        self.student = Student.objects.create(user=user)
        self.student.save()

        user2 = User.objects.create(username="pseudonym")
        self.student_no_resources = Student.objects.create(user=user2)
        self.student_no_resources.save()

        list_resources = []
        resource_number = {}

        for i in range(0, 100):
            gen_resource = "ressource" + str(i)
            resource = Resource.objects.create(content={gen_resource: gen_resource})
            resource.save()
            list_resources.append(resource)

        random.seed()

        for i in range(0, 75):

            for resource in list_resources:

                if random.randint(0, 1) == 1:
                    resource_student = ResourceStudent.objects.create(resource=resource,
                                                                      student=self.student,
                                                                      when=timezone.now())
                    resource_student.save()
                    if str(resource_student) in resource_number:
                        resource_number[str(resource)] += 1
                    else:
                        resource_number[str(resource)] = 1

        self.expected_resource_accessed = resource_number

    def test_when_student_access_resource(self):

        response = ResourcesViewed(self.student).data

        for key, value in self.expected_resource_accessed.items():
            self.assertIn(key, response)
            self.assertEquals(response[key], value)

    def test_when_student_access_no_resources(self):

        self.assertEqual(len(ResourcesViewed(self.student_no_resources).data), 0)
