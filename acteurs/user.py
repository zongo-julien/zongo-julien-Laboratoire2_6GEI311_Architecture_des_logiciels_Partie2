from __future__ import annotations

from typing import TYPE_CHECKING

from acteurs.utilisateur_systeme import UtilisateurSysteme
from modele.enums import Statut
from modele.exceptions import AccesRefuseException, SuppressionInterditeException
from sessions.session_edition import SessionEdition

if TYPE_CHECKING:
    from modele.ticket import Ticket


class User(UtilisateurSysteme):
    """Utilisateur : crée ses tickets et traite ceux qui lui sont assignés."""

    @property
    def role(self) -> str:
        return "User"

    def createTicket(self, ticket: Ticket) -> None:
        ticket.definirCreateur(self)
        self._systeme.ajouterTicket(ticket)

    def supprimerTicket(self, ticket: Ticket) -> None:
        """Suppression directe dans le dépôt, sans passer par la machine à états."""
        if ticket.creator is not self:
            raise AccesRefuseException(
                f"{self._name} n'est pas le créateur du ticket {ticket.ticketID}"
            )
        if ticket.aDejaEteAssigne:
            raise SuppressionInterditeException(
                f"Le ticket {ticket.ticketID} a déjà été assigné : suppression interdite"
            )
        self._systeme.retirerTicket(ticket)

    def soumettreValidation(self, ticket: Ticket) -> None:
        if ticket.assignedUser is not self:
            raise AccesRefuseException(
                f"{self._name} n'est pas l'assigné du ticket {ticket.ticketID}"
            )
        ticket.updateStatus(Statut.VALIDATION)

    def ouvrirSessionEdition(self, ticket: Ticket) -> SessionEdition:
        if ticket.creator is not self:
            raise AccesRefuseException(
                f"{self._name} n'est pas le créateur du ticket {ticket.ticketID} : "
                f"session d'édition refusée"
            )
        return SessionEdition(self, ticket, self._systeme)

    def mesTickets(self, ids: list[int] | None = None) -> list[Ticket]:
        """Tickets créés par cet utilisateur, éventuellement filtrés par identifiant."""
        tickets = self._systeme.ticketsDe(self)
        if ids is None:
            return tickets
        return [ticket for ticket in tickets if ticket.ticketID in ids]
