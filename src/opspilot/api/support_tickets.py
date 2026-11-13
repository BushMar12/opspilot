from fastapi import APIRouter, HTTPException, status

from opspilot.models import SupportTicket, SupportTicketCreate
from opspilot.services.support_tickets import SupportTicketService
from opspilot.repositories.support_tickets import InMemorySupportTicketRepository


router = APIRouter(
    prefix="/support-tickets",
    tags=["support-tickets"],
)

repository = InMemorySupportTicketRepository()
service = SupportTicketService(repository=repository)

@router.post(
    "",
    response_model=SupportTicket,
    status_code=status.HTTP_201_CREATED,
)
def create_support_ticket(ticket_data: SupportTicketCreate) -> SupportTicket:
    return service.create_ticket(ticket_data)


@router.get("/{ticket_id}", response_model=SupportTicket)
def get_support_ticket(ticket_id: str) -> SupportTicket:
    ticket = service.get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=f"Support ticket {ticket_id} not found",
        )
    return ticket

@router.post("/{ticket_id}/resolve", response_model=SupportTicket)
def resolve_support_ticket(ticket_id: str) -> SupportTicket:
    try:
        ticket = service.resolve_ticket(ticket_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
        
        
    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=f"Support ticket {ticket_id} not found",
        )

    return ticket