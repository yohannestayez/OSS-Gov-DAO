class User:
    """Represents a user in the DAO with a specific role and voice credits."""
    def __init__(self, user_id, voice_credits, role="CommunityMember"):
        self.user_id = user_id
        self.voice_credits = voice_credits
        self.role = role # e.g., "Contributor", "Maintainer", "CommunityMember"

    def __repr__(self):
        return f"User({self.user_id}, Role: {self.role}, Credits: {self.voice_credits})" 