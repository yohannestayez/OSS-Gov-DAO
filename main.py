from core.user import User
from core.proposal import Proposal
from core.dao import DAO

if __name__ == "__main__":
    print("Initializing OSS-Gov DAO Simulation...")
    dao = DAO(approval_threshold=18.0, quorum_minimum_voters=2, initial_treasury_funds=1000)
    dao.print_treasury_balance()

    user_alice = User("Alice", 100, role="Maintainer")
    user_bob = User("Bob", 150, role="Contributor")
    user_carol = User("Carol", 50, role="CommunityMember")
    user_dave = User("Dave", 80, role="Contributor")
    user_eve = User("Eve", 40, role="CommunityMember")

    dao.add_user(user_alice)
    dao.add_user(user_bob)
    dao.add_user(user_carol)
    dao.add_user(user_dave)
    dao.add_user(user_eve)
    
    print("\n--- Users in DAO ---")
    for user_id in dao.users:
        print(dao.users[user_id])
    print("--------------------\n")

    prop1_obj = dao.create_proposal("Implement new UI theme for the project", "Alice")
    prop2_obj = dao.create_proposal("Acquire new server for CI/CD pipeline", "Bob", 
                                  is_funding_proposal=True, requested_amount=100)
    prop3_obj = dao.create_proposal("Review minor documentation typos", "Carol")
    prop4_obj = dao.create_proposal("Host a global developer conference (High Cost)", "Dave",
                                  is_funding_proposal=True, requested_amount=2000)

    if not all([prop1_obj, prop2_obj, prop3_obj, prop4_obj]):
        print("Error in proposal creation, exiting simulation.")
        exit()
    
    prop1_id = prop1_obj.proposal_id
    prop2_id = prop2_obj.proposal_id
    prop3_id = prop3_obj.proposal_id
    prop4_id = prop4_obj.proposal_id

    print("\n--- Initial Proposals ---")
    for pid in [prop1_id, prop2_id, prop3_id, prop4_id]:
        dao.print_proposal_details(pid)
    print("------------------------\n")
    dao.print_treasury_balance()

    for pid in [prop1_id, prop2_id, prop3_id, prop4_id]:
        dao.open_voting(pid)

    print(f"--- Voting on Proposal {prop1_id} (UI Theme) ---")
    dao.cast_vote(prop1_id, "Alice", 5)
    dao.cast_vote(prop1_id, "Bob", 4)
    dao.cast_vote(prop1_id, "Carol", 3)
    dao.cast_vote(prop1_id, "Dave", 4)
    print("-------------------------------------------\n")

    print(f"--- Voting on Proposal {prop2_id} (Funding: New Server) ---")
    dao.cast_vote(prop2_id, "Bob", 7)
    dao.cast_vote(prop2_id, "Alice", 6)
    dao.cast_vote(prop2_id, "Dave", 5)
    print("----------------------------------------------------------\n")

    print(f"--- Voting on Proposal {prop3_id} (Doc Typos - Quorum Test) ---")
    dao.cast_vote(prop3_id, "Eve", 2)
    print("------------------------------------------------------------\n")
    
    print(f"--- Voting on Proposal {prop4_id} (Funding: Conference - Insufficient Funds Test) ---")
    dao.cast_vote(prop4_id, "Bob", 9)
    dao.cast_vote(prop4_id, "Alice", 6)
    dao.cast_vote(prop4_id, "Dave", 4)
    print("-------------------------------------------------------------------------------------\n")

    print("--- Closing Voting & Tallying Results ---")
    for pid in [prop1_id, prop2_id, prop3_id, prop4_id]:
        dao.close_voting_and_tally(pid)
        dao.print_proposal_details(pid)
        dao.print_treasury_balance() 
    print("----------------------------------------\n")

    print("--- Final User Voice Credits ---")
    for user_id in dao.users:
        print(dao.users[user_id])
    print("-------------------------------\n")
    
    print("DAO Simulation Complete.")