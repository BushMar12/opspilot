from fastapi import APIRouter, HTTPException, status

from opspilot.models import SupportTicket, SupportTicketCreate


router = APIRouter(
    prefix="/support-tickets",
    tags=["support-tickets"],
)


support_tickets: dict[str, SupportTicket] = {}


@router.post(
    "",
    response_model=SupportTicket,
    status_code=status.HTTP_201_CREATED,
)
def create_support_ticket(ticket_data: SupportTicketCreate) -> SupportTicket:
    ticket_id = f"TKT-{len(support_tickets) + 1:04d}"

    ticket = SupportTicket(
        ticket_id=ticket_id,
        customer_id=ticket_data.customer_id,
        order_id=ticket_data.order_id,
        subject=ticket_data.subject,
        description=ticket_data.description,
        status="open",
    )

    support_tickets[ticket_id] = ticket

    return ticket

@router.get("/{ticket_id}", response_model=SupportTicket)
def get_support_ticket(ticket_id: str) -> SupportTicket:
    ticket = support_tickets.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=f"Support ticket {ticket_id} not found",
        )

    return ticket