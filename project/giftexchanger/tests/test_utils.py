from giftexchanger.tests._utils import GiftExchangeTestCase


class TestAssignmentUtil(GiftExchangeTestCase):

    def test_assignment_util(self):
        test_participants = self.upcoming_exchange_main.participants
        test_non_participants = self.upcoming_exchange_secondary.participants
        for user in self.test_users:
            self.assertIn(user, test_participants)
            self.assertNotIn(user, test_non_participants)

        assignments = self.upcoming_exchange_main.generate_assignments(max_tries=None)
        self.assertEqual(len(assignments), len(test_participants))

        self.fail("not implemented")
