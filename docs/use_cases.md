# OpsPilot Use Cases

## UC-001 — Search Company Policy

### Primary Actor
Customer Support Specialist

### Goal
Retrieve relevant internal company policy information in response to a natural-language question.

### Preconditions
- The user is authorised to access OpsPilot.
- The company policy knowledge base is available.
- Relevant policy documents have been ingested into the system.

### Trigger
The user submits a natural-language question about company policy.

### Main Flow
1. The user submits a policy-related question.
2. OpsPilot interprets the information request.
3. OpsPilot searches the internal policy knowledge base.
4. The system retrieves the most relevant policy sections.
5. OpsPilot generates a concise response based only on retrieved evidence.
6. The system returns the answer together with citations to the relevant policy sections.

### Alternative Flows

#### A1 — No relevant policy found
1. The retrieval system fails to identify sufficiently relevant evidence.
2. OpsPilot informs the user that it cannot answer reliably from the available policy information.
3. No unsupported policy claim is generated.

### Postconditions
- The user receives either a policy-grounded answer with citations or an explicit indication that sufficient evidence was not found.


## UC-002 — Investigate Customer and Order

### Primary Actor
Customer Support Specialist

### Goal
Retrieve and summarise customer and order information needed to investigate a support request.

### Preconditions
- The user is authorised to access customer and order information.
- Customer and order services are available.

### Trigger
The user asks OpsPilot to investigate a customer or order.

### Main Flow
1. The user submits a request containing a customer ID, order ID, or sufficient identifying context.
2. OpsPilot determines what business information is required.
3. The system retrieves customer information from the customer service.
4. The system retrieves relevant order information from the order service.
5. OpsPilot produces a concise summary based on the retrieved structured data.
6. The system returns the summary to the user.

### Alternative Flows

#### A1 — Customer not found
1. The customer lookup returns no matching record.
2. OpsPilot informs the user that the customer could not be found.
3. The workflow stops without inventing customer information.

#### A2 — Order not found
1. The order lookup returns no matching record.
2. OpsPilot informs the user that the order could not be found.
3. The workflow stops or requests additional information where appropriate.

### Postconditions
- The user receives a summary based only on retrieved business data.
- No business action has been executed.


## UC-003 — Evaluate Refund Request

### Primary Actor
Customer Support Specialist

### Goal
Determine whether a customer appears eligible for a refund and recommend the appropriate action.

### Preconditions
- The user is authorised to investigate refunds.
- The relevant customer and order exist.
- Refund policy documents are available.
- Order information is available.

### Trigger
The user submits a request asking whether a customer should receive a refund.

### Main Flow
1. The user provides a natural-language description of the refund request.
2. OpsPilot identifies the relevant customer and order.
3. The system retrieves the current order information.
4. OpsPilot retrieves the relevant refund policy sections.
5. Deterministic business logic calculates any relevant values, including the potential refund amount.
6. OpsPilot combines the customer request, retrieved business data, policy evidence, and deterministic business-rule results.
7. The system generates a refund recommendation.
8. The recommendation includes:
   - eligibility outcome;
   - supporting reason;
   - relevant policy citation;
   - proposed refund amount where applicable;
   - whether further approval is required.
9. The recommendation is returned to the user.

### Alternative Flows

#### A1 — Refund window expired
1. Retrieved order data indicates that the permitted refund period has expired.
2. OpsPilot recommends that the refund is not eligible under the identified policy.
3. The applicable policy evidence is returned.

#### A2 — Insufficient information
1. Required business information or policy evidence is missing.
2. OpsPilot does not make a definitive refund recommendation.
3. The system identifies the missing information.

#### A3 — Approval required
1. Deterministic business logic identifies that the proposed refund requires manager approval.
2. The workflow proceeds to UC-004.

### Postconditions
- A refund recommendation has been generated.
- Supporting evidence is recorded.
- No high-risk refund is executed without required approval.


## UC-004 — Approve High-Value Refund

### Primary Actors
Customer Support Specialist and Support Manager

### Goal
Ensure that refunds above the configured risk threshold require explicit human approval before execution.

### Preconditions
- A valid refund recommendation exists.
- The proposed refund exceeds the configured approval threshold.
- The manager has permission to approve or reject refunds.

### Trigger
UC-003 identifies that manager approval is required.

### Main Flow
1. OpsPilot creates an approval request containing:
   - customer;
   - order;
   - proposed refund amount;
   - recommendation;
   - supporting policy evidence.
2. The approval request is presented to an authorised Support Manager.
3. The manager reviews the recommendation and supporting evidence.
4. The manager explicitly approves the request.
5. The approval decision is recorded in the audit trail.
6. The approved refund becomes eligible for execution by the appropriate business service.

### Alternative Flows

#### A1 — Manager rejects request
1. The manager rejects the approval request.
2. The rejection and optional reason are recorded.
3. The refund is not executed.

#### A2 — Approval remains pending
1. No manager decision has been made.
2. The refund remains blocked from execution.

### Postconditions
- The approval decision is recorded.
- High-value refunds cannot be executed without the required authorisation.