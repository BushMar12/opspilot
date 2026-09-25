Functional requirements

FR-001
The system shall retrieve customer information.

FR-002
The system shall retrieve order information.

FR-003
The system shall search company policies.

Non-functional requirements

NFR-001
API requests should return within X ms excluding LLM requests.

NFR-002
Sensitive actions must require appropriate authorisation.

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