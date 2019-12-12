import random


class ExchangeAssigner(object):

    def __init__(self, exchange_obj):
        self.status = 'pending'
        self.status_message = 'assignments not yet executed'
        self.exchange_obj = exchange_obj
        self.assignment_map = {}

    def _check_is_closed_loop(self, assignments):
        # edges = []
        checking_now = list(assignments.keys())[0]
        checking_next = assignments[checking_now]
        checked = []
        while checking_now:
            checked.append(checking_now)
            checking_now = checking_next
            checking_next = assignments.get(checking_next)
            if checking_next in checked:
                checked.append(checking_next)
                # loop has closed, stop creating edges and end while loop
                checking_now = False

        # if we made the same amount of edges as we have assignments, then
        # the while loop got all the way through the assignments and we have
        # a full loop
        return len(checked) == len(assignments)

    def _do_assignments(self):
        assignments = {}
        recipients = []
        for giver in self.exchange_obj.participants:
            available_recipients_for_user = []
            for user in self.exchange_obj.participants:
                if user != giver and user not in recipients:
                    available_recipients_for_user.append(user)

            if not available_recipients_for_user:
                is_closed_loop = self._check_is_closed_loop(assignments)
                if is_closed_loop:
                    self.assignment_map = assignments
                    return True
                else:
                    return False
            else:
                recipient = random.choice(available_recipients_for_user)
                assignments[giver.id] = recipient.id
                recipients.append(recipient)

    def make_assignments(self, max_tries=6):
        if len(self.exchange_obj.participants) < 3:
            raise Exception("Not enough participants. Needs at last 3.")
        is_closed_loop = False
        tries = 0
        while not is_closed_loop:
            is_closed_loop = self._do_assignments()
            tries += 1
            if max_tries and tries == max_tries:
                raise Exception("Max tries reached")
