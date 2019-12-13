import random
from copy import deepcopy


class ExchangeAssigner(object):

    def __init__(self, exchange_obj):
        self.status = 'Pending'
        self.status_message = 'Assignments not yet mapped'
        self.exchange_obj = exchange_obj
        self.assignment_map = {}

    def _check_is_closed_loop(self, debug=False):
        """
        [3, 7, 6, 2, 5, 1, 8], giver: 4 recv: 8
        [4, 7, 6, 2, 5, 1], giver: 3 recv: 4
        [3, 6, 2, 5, 1], giver: 7 recv: 1
        [3, 7, 2, 5], giver: 6 recv: 2
        [3, 7, 6, 5], giver: 2 recv: 7
        [3, 6], giver: 5 recv: 6
        [3, 5], giver: 1 recv: 3
        [5], giver: 8 recv: 5

        4->8, 8->5, 5->6, 6->2, 2->7, 7->1, 1->3, 3->4


        """
        check_next = list(self.assignment_map.keys())[0]
        # [4, 8, 5, 6, 2, 7, 1, 3] -> 4

        # 8
        checked_givers = []
        checking = True
        while checking:
            checked_givers.append(check_next)
            if debug:
                print("{} has {}".format(check_next, self.assignment_map.get(check_next)))
            
            check_next = self.assignment_map.get(check_next)
            if check_next in checked_givers:
                # loop has closed, stop creating edges and end while loop
                checking = False
                if debug: 
                    print("loop closed")

        # if we made the same amount of edges as we have assignments, then
        # the while loop got all the way through the assignments and we have
        # a full loop
        if debug:
            print("assg count: {}".format(len(checked_givers)))
        return len(checked_givers) == len(self.assignment_map)

    def _do_assignments(self, debug=False):
        assignments = []
        recipients = []
        participants = deepcopy(self.exchange_obj.participants)
        if debug:
            print("-----------------------------")
            print(participants)
        for giver in participants:
            available_recipients_for_user = [p.id for p in participants if p != giver and p.id not in recipients]
            if not available_recipients_for_user:
                # the only remaining recipient was the giver so bail
                return False
            else:
                recipient_id = random.choice(available_recipients_for_user)
                assignments.append((giver.id, recipient_id))
                recipients.append(recipient_id)
                if debug:
                    print("assigned {} to {} from {}".format(giver.id, recipient_id, available_recipients_for_user))

        # everyone got assigned, check if closed loop
        self.assignment_map = assignments_dict = {g: r for g, r in assignments}
        is_closed_loop = self._check_is_closed_loop(debug)
        if is_closed_loop:
            if debug:
                print("{}".format(self.assignment_map))
            return True
        else:
            return False

    def make_assignments(self, max_tries=6, debug=False):
        if len(self.exchange_obj.participants) < 3:
            raise Exception("Not enough participants. Needs at last 3.")
        is_closed_loop = False
        tries = 0
        self.status = 'Working'
        self.status_message = 'Mapping assignments'
        while not is_closed_loop:
            is_closed_loop = self._do_assignments(debug)
            tries += 1
            if max_tries and tries == max_tries:
                self.status = 'Failed'
                self.status_message = 'Could not set closed loop in max tries'
                raise Exception("Max tries reached")
        self.status = 'Complete'
        self.status_message = 'Mapped assignments'
