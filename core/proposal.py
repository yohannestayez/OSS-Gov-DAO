import math

class Proposal:
    """Represents a proposal in the DAO."""
    # Possible statuses for a proposal
    PENDING = "PENDING"
    VOTING = "VOTING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"

    def __init__(self, proposal_id, description, proposer_id, is_funding_proposal=False, requested_amount=0):
        self.proposal_id = proposal_id
        self.description = description
        self.proposer_id = proposer_id
        # Stores votes as {user_id: number_of_voice_credits_committed}
        self.votes = {}
        # Stores the calculated quadratic weight for each vote {user_id: qv_weight}
        self.quadratic_votes = {}
        self.status = Proposal.PENDING
        self.total_quadratic_score = 0
        self.is_funding_proposal = is_funding_proposal
        self.requested_amount = requested_amount
        if self.is_funding_proposal and self.requested_amount <= 0:
            # Basic validation for funding proposals
            raise ValueError("Funding proposals must have a positive requested amount.")

    def add_vote(self, user, num_credits_committed):
        """Adds a user's vote to the proposal."""
        if user.user_id in self.votes:
            print(f"User {user.user_id} has already voted on proposal {self.proposal_id}.")
            return False
        if num_credits_committed <= 0:
            print("Number of credits committed must be positive.")
            return False
        # Note: The user object passed here will be from core.user
        # Its voice_credits attribute will be checked and updated.
        if user.voice_credits < num_credits_committed**2:
            print(f"User {user.user_id} does not have enough voice credits (needs {num_credits_committed**2}, has {user.voice_credits}).")
            return False

        user.voice_credits -= num_credits_committed**2  # Cost is credits squared
        self.votes[user.user_id] = num_credits_committed
        self.quadratic_votes[user.user_id] = num_credits_committed
        print(f"User {user.user_id} voted with {num_credits_committed} credits (cost: {num_credits_committed**2}) on proposal {self.proposal_id}. Remaining credits: {user.voice_credits}")
        return True

    def calculate_total_quadratic_score(self):
        """Calculates the total quadratic score for the proposal."""
        self.total_quadratic_score = sum(self.quadratic_votes.values())
        return self.total_quadratic_score

    def __repr__(self):
        funding_info = ""
        if self.is_funding_proposal:
            funding_info = f", Funding Request: {self.requested_amount} units"
        return f"Proposal({self.proposal_id}, '{self.description}', Proposer: {self.proposer_id}, Status: {self.status}, QV Score: {self.total_quadratic_score:.2f}{funding_info})" 