from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from modele.exceptions import TransitionInvalideException

if TYPE_CHECKING:
    from modele.enums import Statut
    from modele.ticket import Ticket


class EtatTicket(ABC):
    """État abstrait d'un ticket (patron State)."""

    @property
    @abstractmethod
    def nom(self) -> Statut:
        """Statut correspondant à cet état."""

    def gererTransition(self, ticket: Ticket, nouveau_statut: Statut) -> None:
        """Comportement par défaut : toute transition est refusée."""
        raise TransitionInvalideException(self.nom, nouveau_statut)
