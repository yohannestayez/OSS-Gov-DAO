## Project Overview

The OSS-Gov DAO is a prototype demonstrating a Decentralized Autonomous Organization specifically designed for governing open-source software projects. The project implements a governance model that includes various stakeholders, a defined decision flow, and Quadratic Voting as the primary voting mechanism.

## Features

*   **User Management:** Add users with distinct roles and voice credits.
*   **Proposal System:** Create standard and funding proposals.
*   **Quadratic Voting (QV):** A voting mechanism where the number of votes a user can cast for a proposal is the square root of the voice credits they commit, and the cost to their voice credits is the square of the credits committed for that vote. This aims to balance influence and encourage broader participation.
*   **Decision Flow:** Clearly defined lifecycle for proposals (Pending -> Voting -> Approved/Rejected -> Executed).
*   **Quorum Requirement:** Minimum number of unique voters needed for a proposal to be considered valid.
*   **Approval Threshold:** Minimum QV score a proposal needs to pass.
*   **Treasury Management:** DAO maintains a treasury, and funding proposals can request funds, which are disbursed upon approval if available.
*   **Simulation:** The `main.py` script provides a simulation of the DAO's operations, showcasing user creation, proposal submission, voting, and execution.

## How it Works

The DAO operates through a structured process:

1.  **Stakeholders (Users):**
    *   Individuals participate as users within the DAO.
    *   Each user is assigned an ID, initial `voice_credits`, and a role.
    *   Roles include: `Maintainer`, `Contributor`, `CommunityMember`. (Currently, roles are descriptive and don't alter core mechanics but can be extended).
    *   `voice_credits` represent a user's potential influence or voting power pool.

2.  **Proposal Process:**
    *   Any registered user can create a proposal.
    *   Proposals have a description and an ID.
    *   **Funding Proposals:** Can be created to request a specific amount from the DAO's treasury.
    *   Initially, proposals are in `PENDING` status.

3.  **Voting Mechanism:**
    *   Proposals are moved to the `VOTING` status to allow users to cast votes.
    *   Users commit a certain number of "credits" (let's call this `X`) towards a specific proposal.
    *   **Vote Weight (QV Score Contribution):** The influence of the vote is `sqrt(X)`.
    *   **Cost:** Committing `X` to a vote deducts `X^2` from the user's total `voice_credits`.
    *   A user can vote only once per proposal.

4.  **Decision and Execution:**
    *   **Closing Vote:** After the voting period, votes are tallied.
    *   **Quorum Check:** The system checks if the `quorum_minimum_voters` has been met. If not, the proposal is `REJECTED`.
    *   **Tallying:** If quorum is met, the total QV score (sum of all `(X)` from votes) is calculated.
    *   **Approval:** If the total QV score meets or exceeds the `approval_threshold`, the proposal is `APPROVED`. Otherwise, it's `REJECTED`.
    *   **Execution:**
        *   Approved non-funding proposals are marked as `EXECUTED`.
        *   Approved funding proposals are `EXECUTED` if the treasury has sufficient funds; the requested amount is transferred from the treasury. If funds are insufficient, the proposal remains `APPROVED` but is not executed.