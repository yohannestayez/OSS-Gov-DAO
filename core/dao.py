from .user import User
from .proposal import Proposal

class DAO:
    """Manages users, proposals, and the voting process for the DAO."""
    def __init__(self, approval_threshold=10, quorum_minimum_voters=1, initial_treasury_funds=0):
        self.users = {}  # {user_id: User_object}
        self.proposals = {} # {proposal_id: Proposal_object}
        self.next_proposal_id = 1
        self.approval_threshold = approval_threshold # QV score needed for a proposal to be approved
        self.quorum_minimum_voters = quorum_minimum_voters # Min number of unique voters for validity
        self.treasury_funds = initial_treasury_funds
        print(f"DAO initialized with Approval Threshold: {approval_threshold}, Quorum: {quorum_minimum_voters} voters, Treasury: {initial_treasury_funds} units.")

    def add_user(self, user):
        """Adds a user to the DAO."""
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            print(f"User {user.user_id} ({user.role}) added to the DAO with {user.voice_credits} credits.")
        else:
            print(f"User {user.user_id} already exists.")

    def create_proposal(self, description, proposer_id, is_funding_proposal=False, requested_amount=0):
        """Creates a new proposal, optionally a funding proposal."""
        if proposer_id not in self.users:
            print(f"Proposer {proposer_id} is not a registered user in the DAO.")
            return None
        
        try:
            proposal_id = self.next_proposal_id
            proposal = Proposal(proposal_id, description, proposer_id, is_funding_proposal, requested_amount)
            self.proposals[proposal_id] = proposal
            self.next_proposal_id += 1
            funding_status = f" (Funding Request: {requested_amount} units)" if is_funding_proposal else ""
            print(f"Proposal {proposal_id}: '{description}' by {proposer_id}{funding_status}. Status: {proposal.status}")
            return proposal
        except ValueError as e:
            print(f"Error creating proposal: {e}")
            return None

    def open_voting(self, proposal_id):
        """Opens a proposal for voting."""
        if proposal_id in self.proposals:
            proposal = self.proposals[proposal_id]
            if proposal.status == Proposal.PENDING:
                proposal.status = Proposal.VOTING
                print(f"Proposal {proposal_id} is now open for voting.")
            else:
                print(f"Proposal {proposal_id} cannot be opened for voting. Current status: {proposal.status}")
        else:
            print(f"Proposal {proposal_id} not found.")

    def cast_vote(self, proposal_id, user_id, num_credits_committed):
        """Allows a user to cast a vote on a proposal."""
        if proposal_id not in self.proposals:
            print(f"Proposal {proposal_id} not found.")
            return False
        if user_id not in self.users:
            print(f"User {user_id} not found.")
            return False

        proposal = self.proposals[proposal_id]
        user = self.users[user_id]

        if proposal.status != Proposal.VOTING:
            print(f"Proposal {proposal_id} is not open for voting. Current status: {proposal.status}")
            return False

        return proposal.add_vote(user, num_credits_committed)

    def close_voting_and_tally(self, proposal_id):
        """Closes voting, checks quorum, tallies votes, and determines outcome."""
        if proposal_id not in self.proposals:
            print(f"Proposal {proposal_id} not found.")
            return
        
        proposal = self.proposals[proposal_id]
        if proposal.status != Proposal.VOTING:
            print(f"Proposal {proposal_id} is not in the VOTING state. Current status: {proposal.status}")
            return

        num_voters = len(proposal.votes)
        print(f"Voting closed for Proposal {proposal_id}. Number of unique voters: {num_voters}.")

        if num_voters < self.quorum_minimum_voters:
            proposal.status = Proposal.REJECTED
            print(f"Proposal {proposal_id} REJECTED due to not meeting quorum (Voters: {num_voters}, Quorum: {self.quorum_minimum_voters}).")
            return

        score = proposal.calculate_total_quadratic_score()
        print(f"Proposal {proposal_id} met quorum. Total QV Score: {score:.2f}")

        if score >= self.approval_threshold:
            proposal.status = Proposal.APPROVED
            print(f"Proposal {proposal_id} APPROVED.")
            self.execute_proposal(proposal_id) # Attempt to execute immediately
        else:
            proposal.status = Proposal.REJECTED
            print(f"Proposal {proposal_id} REJECTED. Score {score:.2f} is below threshold {self.approval_threshold}.")
            
    def execute_proposal(self, proposal_id):
        """Simulates the execution of an approved proposal, handling funding if applicable."""
        if proposal_id not in self.proposals:
            print(f"Proposal {proposal_id} not found.")
            return

        proposal = self.proposals[proposal_id]
        if proposal.status != Proposal.APPROVED:
            print(f"Proposal {proposal_id} cannot be executed. Status: {proposal.status}")
            return

        if proposal.is_funding_proposal:
            if self.treasury_funds >= proposal.requested_amount:
                self.treasury_funds -= proposal.requested_amount
                proposal.status = Proposal.EXECUTED
                print(f"Proposal {proposal_id} ({proposal.description}) EXECUTED. {proposal.requested_amount} units disbursed from treasury. Treasury balance: {self.treasury_funds}")
            else:
                # Not enough funds, could mark as FAILED_EXECUTION or similar
                print(f"Proposal {proposal_id} ({proposal.description}) EXECUTION FAILED. Insufficient treasury funds (Needs: {proposal.requested_amount}, Has: {self.treasury_funds}). Proposal remains APPROVED but not executed.")
                # Optionally, change status to something like Proposal.EXECUTION_FAILED
                return # Don't set to EXECUTED if funds are insufficient
        else:
            # Non-funding proposal execution
            proposal.status = Proposal.EXECUTED
            print(f"Proposal {proposal_id} ({proposal.description}) has been EXECUTED.")
            
    def print_proposal_details(self, proposal_id):
        if proposal_id in self.proposals:
            proposal = self.proposals[proposal_id]
            print(f"\n--- Proposal {proposal_id} Details ---")
            print(f"Description: {proposal.description}")
            print(f"Proposer: {proposal.proposer_id}")
            print(f"Status: {proposal.status}")
            funding_req = f", Requested: {proposal.requested_amount} units" if proposal.is_funding_proposal else ""
            print(f"Type: {'Funding' if proposal.is_funding_proposal else 'Standard'}{funding_req}")
            print(f"Total QV Score: {proposal.total_quadratic_score:.2f} (Approval: >={self.approval_threshold})")
            print(f"Voters: {len(proposal.votes)} (Quorum: >={self.quorum_minimum_voters})")
            if proposal.votes:
                print("Votes (User: Credits Committed -> QV Weight):")
                for user_id, credits in proposal.votes.items():
                    print(f"  - {user_id}: {credits} -> {proposal.quadratic_votes[user_id]:.2f}")
            else:
                print("No votes cast yet.")
            print("---------------------------\n")
        else:
            print(f"Proposal {proposal_id} not found.")

    def print_treasury_balance(self):
        print(f"\n--- DAO Treasury Balance: {self.treasury_funds} units ---") 