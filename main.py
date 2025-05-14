from core.user import User
from core.proposal import Proposal # For Proposal.STATUS constants if used, though DAO handles instantiation
from core.dao import DAO

# --- Main Simulation ---
if __name__ == "__main__":
    print("Initializing OSS-Gov DAO Simulation...")
    dao = DAO(approval_threshold=7.0, quorum_minimum_voters=2, initial_treasury_funds=1000)
    dao.print_treasury_balance()

    # 1. Add Users
    user_alice = User("Alice", 100, role="Maintainer")
    user_bob = User("Bob", 150, role="Contributor")
    user_carol = User("Carol", 50, role="CommunityMember") # Increased Carol's credits
    user_dave = User("Dave", 80, role="Contributor")    # Increased Dave's credits
    user_eve = User("Eve", 40, role="CommunityMember")      # Increased Eve's credits

    dao.add_user(user_alice)
    dao.add_user(user_bob)
    dao.add_user(user_carol)
    dao.add_user(user_dave)
    dao.add_user(user_eve)
    
    print("\n--- Users in DAO ---")
    for user_id in dao.users:
        print(dao.users[user_id])
    print("--------------------\n")

    # 2. Create Proposals
    prop1_obj = dao.create_proposal("Implement new UI theme for the project", "Alice")
    prop2_obj = dao.create_proposal("Acquire new server for CI/CD pipeline", "Bob", 
                                  is_funding_proposal=True, requested_amount=100)
    prop3_obj = dao.create_proposal("Review minor documentation typos", "Carol") # Quorum test
    prop4_obj = dao.create_proposal("Host a global developer conference (High Cost)", "Dave",
                                  is_funding_proposal=True, requested_amount=2000) # Insufficient funds test

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

    # 3. Open Proposals for Voting
    for pid in [prop1_id, prop2_id, prop3_id, prop4_id]:
        dao.open_voting(pid)
    print("")

    # 4. Users Cast Votes
    print(f"--- Voting on Proposal {prop1_id} (UI Theme) ---")
    dao.cast_vote(prop1_id, "Alice", 5)  # Cost 25, QV 2.23
    dao.cast_vote(prop1_id, "Bob", 4)    # Cost 16, QV 2.00
    dao.cast_vote(prop1_id, "Carol", 3)  # Cost 9,  QV 1.73
    dao.cast_vote(prop1_id, "Dave", 4)   # Cost 16, QV 2.00
    # Voters: 4 (>=2), QV: 7.96 (>=7.0) -> PASS
    print("-------------------------------------------\n")

    print(f"--- Voting on Proposal {prop2_id} (Funding: New Server) ---")
    dao.cast_vote(prop2_id, "Bob", 7)    # Cost 49, QV 2.64
    dao.cast_vote(prop2_id, "Alice", 6)  # Cost 36, QV 2.45
    dao.cast_vote(prop2_id, "Dave", 5)   # Cost 25, QV 2.23
    # Voters: 3 (>=2), QV: 7.32 (>=7.0) -> PASS, treasury deducts 100
    print("----------------------------------------------------------\n")

    print(f"--- Voting on Proposal {prop3_id} (Doc Typos - Quorum Test) ---")
    dao.cast_vote(prop3_id, "Eve", 2)    # Cost 4, QV 1.41
    # Voters: 1 (<2) -> FAIL (Quorum not met)
    print("------------------------------------------------------------\n")
    
    print(f"--- Voting on Proposal {prop4_id} (Funding: Conference - Insufficient Funds Test) ---")
    # Goal: Pass Quorum (>=2) and QV Threshold (>=7.0) to test execution failure due to funds.
    # Alice (remaining: 100-25-36=39), Bob (150-16-49=85), Carol (50-9=41), Dave (80-16-25=39), Eve (40-4=36)
    dao.cast_vote(prop4_id, "Bob", 9)     # Cost 81 (Bob has 85 -> 4 left). QV 3.0
    dao.cast_vote(prop4_id, "Alice", 6)   # Cost 36 (Alice has 39 -> 3 left). QV ~2.45
    dao.cast_vote(prop4_id, "Dave", 4)    # Cost 16 (Dave has 39 -> 23 left). QV 2.0
    # Voters: 3 (>=2). QV: 3.0 + 2.45 + 2.0 = 7.45 (>=7.0) -> PASS voting.
    # Execution should fail due to insufficient funds (needs 2000).
    print("-------------------------------------------------------------------------------------\n")

    # 5. Close Voting and Tally Results
    print("--- Closing Voting & Tallying Results ---")
    for pid in [prop1_id, prop2_id, prop3_id, prop4_id]:
        dao.close_voting_and_tally(pid)
        dao.print_proposal_details(pid)
        dao.print_treasury_balance() 
    print("----------------------------------------\n")

    # 6. Display Final User Credits
    print("--- Final User Voice Credits ---")
    for user_id in dao.users:
        print(dao.users[user_id])
    print("-------------------------------\n")
    
    print("DAO Simulation Complete.")