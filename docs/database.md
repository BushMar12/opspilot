# OpsPilot Database Design

## Initial Database

OpsPilot will use PostgreSQL for persistent relational data.

The first version contains three core tables:

- customers
- orders
- support_tickets

## Relationships

- One customer may have many orders.
- One customer may have many support tickets.
- A support ticket may optionally reference one order.
- Each order belongs to one customer.

## customers

| Column | Type | Constraints |
| --- | --- | --- |
| customer_id | TEXT | PRIMARY KEY |
| name | TEXT | NOT NULL |
| email | TEXT | NOT NULL, UNIQUE |
| account_status | TEXT | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

## orders

| Column | Type | Constraints |
| --- | --- | --- |
| order_id | TEXT | PRIMARY KEY |
| customer_id | TEXT | NOT NULL, FOREIGN KEY |
| status | TEXT | NOT NULL |
| order_date | TIMESTAMP | NOT NULL |
| delivery_date | TIMESTAMP | NULL |
| total_amount | NUMERIC(12,2) | NOT NULL |

## support_tickets

| Column | Type | Constraints |
| --- | --- | --- |
| ticket_id | TEXT | PRIMARY KEY |
| customer_id | TEXT | NOT NULL, FOREIGN KEY |
| order_id | TEXT | NULL, FOREIGN KEY |
| subject | TEXT | NOT NULL |
| description | TEXT | NOT NULL |
| status | TEXT | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

## Integrity Rules

- An order must reference an existing customer.
- A support ticket must reference an existing customer.
- A support ticket may reference an order.
- Financial amounts should use exact decimal storage rather than floating point.
- Business rules such as refund approval thresholds remain in the application/service layer.