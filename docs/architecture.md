# OpsPilot Architecture

## Domain Overview

OpsPilot supports customer-support operations for Northstar Commerce, a fictional mid-sized e-commerce company.

The initial domain contains the following core entities:

### Customer

Represents an external customer who purchases products from Northstar Commerce.

A customer may have multiple orders and multiple support tickets.

### Order

Represents a purchase made by a customer.

Each order belongs to one customer and may contain multiple order items.

An order may have zero or more associated refunds.

### OrderItem

Represents an individual line item within an order.

An order item records product information, quantity and the price paid at the time of purchase.

### Refund

Represents a requested, pending, rejected or completed monetary refund associated with an order.

A refund may require explicit human approval depending on applicable business rules.

### ApprovalRequest

Represents a human authorisation request for a sensitive business action.

The initial implementation will use approval requests primarily for high-value refunds.

An approval request may be pending, approved or rejected.

### PolicyDocument

Represents an authoritative Northstar Commerce internal policy document.

Examples include refund, warranty, shipping and escalation policies.

Policy documents will later provide the source material for the OpsPilot retrieval-augmented generation knowledge system.

### SupportTicket

Represents a customer-support issue or request.

A support ticket may reference a customer and an order and provides natural-language context that OpsPilot may analyse.

### User

Represents an internal Northstar Commerce employee who uses OpsPilot.

Initial user roles include:

- Customer Support Specialist
- Support Manager
- System Administrator

### AuditEvent

Represents a record of a significant action or decision occurring within OpsPilot.

Audit events will provide traceability for user actions, AI-assisted recommendations, approval decisions and business-tool execution.


## Core Relationships

The initial domain relationships are:

- One Customer may have many Orders.
- One Customer may have many SupportTickets.
- One Order contains one or more OrderItems.
- One Order may have zero or more Refunds.
- A Refund may require an ApprovalRequest.
- A User may create or decide an ApprovalRequest.
- Significant system actions generate AuditEvents.
- PolicyDocuments provide evidence used during AI-assisted recommendations.


## System Boundary

OpsPilot is an internal AI-assisted operations platform.

### Responsibilities Inside OpsPilot

OpsPilot is responsible for:

- interpreting natural-language operational requests;
- retrieving relevant internal policy information;
- orchestrating calls to business-data services;
- producing AI-assisted operational recommendations;
- applying deterministic business rules where appropriate;
- coordinating human approval workflows;
- recording auditable operational events;
- evaluating and monitoring AI-assisted behaviour.

### Responsibilities Outside OpsPilot

The following systems are considered external sources of truth:

- customer information system;
- order management system;
- payment/refund processing system;
- external identity provider;
- email or notification delivery system.

During development, OpsPilot may use local or mock implementations of these systems rather than real third-party services.

## Source-of-Truth Principle

OpsPilot shall not treat LLM-generated content as authoritative business data.

Structured business facts such as customer identity, order status, delivery dates and refund amounts must originate from authoritative business systems or deterministic calculations.

The LLM may interpret, summarise and explain this information but shall not act as the source of truth for it.

## Architectural Principle

The system should separate:

- business data;
- deterministic business logic;
- AI-assisted reasoning;
- workflow orchestration;
- security and authorisation;
- external integrations.

This separation should allow individual components to be tested and replaced without requiring major changes to unrelated parts of the system.

## Domain Refinement

### RefundRecommendation

OpsPilot does not directly own the financial refund transaction.

Instead, OpsPilot creates a `RefundRecommendation`, which represents the system's proposed operational action based on business data, policy evidence and deterministic rules.

A refund recommendation may contain:

- customer identifier;
- order identifier;
- related support ticket;
- eligibility decision;
- recommended refund amount;
- explanation;
- policy evidence;
- whether approval is required;
- execution status.

The actual financial refund transaction is performed by an external refund or payment service.

This distinction separates AI-assisted decision support from financial execution.

### RefundRecommendation States

The initial states are:

- `CREATED`
- `BLOCKED`
- `EXECUTED`
- `CANCELLED`

A recommendation becomes `BLOCKED` when an external condition prevents execution, such as a required human approval.

A recommendation may become `EXECUTED` only after all required business and authorisation conditions have been satisfied.

A rejected approval may cause the associated recommendation to become `CANCELLED`.


## ApprovalRequest State Model

An approval request represents an explicit human decision required before a sensitive business action can proceed.

Initial states:

- `PENDING`
- `APPROVED`
- `REJECTED`
- `CANCELLED`

Valid transitions:

- `PENDING -> APPROVED`
- `PENDING -> REJECTED`
- `PENDING -> CANCELLED`

For the initial version, approved, rejected and cancelled requests are terminal states.

The system shall prevent invalid approval-state transitions.


## SupportTicket States

The initial support-ticket lifecycle is:

- `OPEN`
- `IN_PROGRESS`
- `RESOLVED`
- `CLOSED`

The order management system remains the source of truth for order status and order-state transitions.


## Audit Events

Audit events represent historical system activity and should be treated as append-only records.

Examples include:

- refund recommendation created;
- approval requested;
- approval approved;
- approval rejected;
- refund execution requested;
- refund execution succeeded;
- refund execution failed;
- policy evidence retrieved;
- sensitive tool invoked.

Audit records should not be rewritten as a substitute for creating a new event.


## State Ownership Principle

OpsPilot shall only control state transitions for entities it owns.

For example:

- OpsPilot controls `RefundRecommendation` state.
- OpsPilot controls `ApprovalRequest` state.
- The external order system controls `Order` state.
- The external refund service controls the actual `RefundTransaction`.

This separation prevents OpsPilot from incorrectly becoming the source of truth for external business systems.