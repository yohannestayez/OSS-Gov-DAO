class User:
    """Represents a user in the DAO with a specific role and voice credits."""
    def __init__(self, user_id, voice_credits, role="CommunityMember"):
        """
        Initializes a new User instance with the specified user ID, voice credits, and role.

        Args:
            user_id: The unique identifier for the user.
            voice_credits: The number of voice credits assigned to the user.
            role (str, optional): The role assigned to the user. Must be one of "Contributor", "Maintainer", or "CommunityMember".
                Defaults to "CommunityMember".
        """
        self.user_id = user_id
        self.voice_credits = voice_credits
        # Validate roles: if the user is not one of these then the user is not accepted
        valid_roles = {"Contributor", "Maintainer", "CommunityMember"}
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")
        self.role = role  # e.g., "Contributor", "Maintainer", "CommunityMember"

    def __repr__(self):
        return f"User({self.user_id}, Role: {self.role}, Credits: {self.voice_credits})" 