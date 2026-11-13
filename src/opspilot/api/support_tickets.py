from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from opspilot.dependencies import get_support_ticket_service

from opspilot.models import SupportTicket, SupportTicketCreate
from opspilot.services.support_tickets import SupportTicketService
from opspilot.repositories.support_tickets import InMemorySupportTicketRepository


router = APIRouter(
    prefix="/support-tickets",
    tags=["support-tickets"],
)

SupportTicketServiceDep = Annotated[SupportTicketService, Depends(get_support_ticket_service)]

@router.post(
    "",
    response_model=SupportTicket,
    status_code=status.HTTP_201_CREATED,
)
def create_support_ticket(ticket_data: SupportTicketCreate, service: SupportTicketServiceDep) -> SupportTicket:
    return service.create_ticket(ticket_data)


@router.get("/{ticket_id}", response_model=SupportTicket)
def get_support_ticket(ticket_id: str, service: SupportTicketServiceDep) -> SupportTicket:
    ticket = service.get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=f"Support ticket {ticket_id} not found",
        )
    return ticket

@router.post("/{ticket_id}/resolve", response_model=SupportTicket)
def resolve_support_ticket(ticket_id: str, service: SupportTicketServiceDep) -> SupportTicket:
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