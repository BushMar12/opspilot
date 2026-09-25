# OpsPilot Requirements

## Business Context

Northstar Commerce is a fictional mid-sized e-commerce company selling consumer electronics online.

Customer-support employees regularly handle operational requests involving customer information, orders, refunds and internal company policies.

Resolving these requests currently requires employees to gather information from multiple systems, manually search internal policy documents, interpret business rules and determine the appropriate action.

This process can be time-consuming, inconsistent and difficult to audit.

## Business Problem

Customer-support specialists need a faster and more reliable way to investigate customer issues, retrieve relevant company policies and determine appropriate operational actions without manually switching between multiple systems.

## Proposed System

OpsPilot will be an AI-assisted internal operations platform that helps customer-support employees investigate customer requests by combining natural-language understanding, company knowledge retrieval and structured business data.

The system may recommend operational actions and invoke approved business tools, but deterministic business rules and human approval will be used where appropriate instead of relying solely on LLM reasoning.

## Initial Scope

The first version of OpsPilot will support four main workflows:

1. Answer questions using internal company policies.
2. Retrieve and summarise customer and order information.
3. Determine refund eligibility and recommend refund actions.
4. Escalate high-value refunds for human approval before execution.

## Primary User

The primary user is a Customer Support Specialist responsible for investigating and resolving customer requests.

Additional roles such as Support Manager and System Administrator may be introduced as required by later project stages.

## Design Principle

OpsPilot will use AI only where probabilistic reasoning, natural-language understanding or semantic knowledge retrieval provides value.

Deterministic business rules, calculations, database operations and security controls will remain implemented using conventional software wherever possible.


## Functional Requirements

### Authentication and Authorisation

**FR-001**  
The system shall identify authenticated users before allowing access to protected business information.

**FR-002**  
The system shall restrict operations according to the user's assigned role and permissions.


### Customer and Order Information

**FR-003**  
The system shall retrieve a customer using a unique customer identifier.

**FR-004**  
The system shall retrieve orders associated with a customer.

**FR-005**  
The system shall retrieve an order using a unique order identifier.

**FR-006**  
The system shall return an explicit not-found result when a requested customer or order does not exist.


### Policy Retrieval

**FR-007**  
The system shall accept natural-language questions relating to internal company policies.

**FR-008**  
The system shall retrieve relevant policy sections from the internal knowledge base.

**FR-009**  
Policy-based answers shall include references to the policy evidence used to generate the response.

**FR-010**  
The system shall avoid generating a definitive policy answer when sufficient supporting evidence cannot be retrieved.


### Refund Evaluation

**FR-011**  
The system shall accept a natural-language customer refund request.

**FR-012**  
The system shall retrieve the relevant customer, order and policy information needed to evaluate the refund request.

**FR-013**  
The system shall calculate refundable amounts using deterministic business logic rather than relying on an LLM for arithmetic or mandatory numerical rules.

**FR-014**  
The system shall generate a refund recommendation based on retrieved business information, relevant policy evidence and deterministic business-rule results.

**FR-015**  
A refund recommendation shall include:
- eligibility outcome;
- explanation;
- supporting policy evidence;
- proposed refund amount where applicable;
- approval status.


### Human Approval

**FR-016**  
The system shall determine whether manager approval is required using deterministic business rules.

**FR-017**  
The system shall create an approval request for refunds that exceed the configured approval threshold.

**FR-018**  
The system shall prevent a high-risk refund from being executed while the required approval is pending or rejected.

**FR-019**  
An authorised manager shall be able to approve or reject an approval request.


### Auditability

**FR-020**  
The system shall record significant operational events in an audit trail.

**FR-021**  
Audit records shall include sufficient information to determine what action occurred, when it occurred and which user or system component initiated it.


## Initial Non-Functional Requirements

### Security

**NFR-001**  
Secrets, API credentials and database passwords shall not be stored directly in source code.

**NFR-002**  
Protected customer and order information shall only be accessible to authorised users.

**NFR-003**  
Sensitive business tools shall operate according to least-privilege permissions.

**NFR-004**  
The system shall validate external inputs before using them in sensitive business operations.


### Reliability

**NFR-005**  
Failure of an AI component shall not result in automatic execution of an unsupported high-risk business action.

**NFR-006**  
The system shall fail safely when required business data or supporting policy evidence is unavailable.


### AI Grounding

**NFR-007**  
Policy-related claims generated by the AI system shall be grounded in retrieved company policy evidence.

**NFR-008**  
The system shall distinguish retrieved business facts from model-generated explanatory text.


### Maintainability

**NFR-009**  
Business logic, API handling, data access and AI orchestration shall be separated into maintainable components.

**NFR-010**  
Major system behaviour shall be covered by automated tests appropriate to the component.


### Observability

**NFR-011**  
The system shall record sufficient logs to diagnose failed workflows without exposing sensitive secrets.

**NFR-012**  
AI workflow execution shall eventually expose measurable information including latency, model usage and failure status.


### Evaluation

**NFR-013**  
AI-assisted components shall be evaluated using reproducible test cases rather than manual demonstration alone.

**NFR-014**  
Changes to AI behaviour shall be testable against a regression evaluation dataset.