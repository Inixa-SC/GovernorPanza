from abc import ABC, abstractmethod
from typing import List

class Verificator(ABC):
    @abstractmethod
    def verify(self, chatml_conversation: List) -> List:
        """Para implementar este método tienes que recibir un chatml con el penúltimo elemento del array con rol <assistant> y el último <verificator>
            verificator tendrá los atributos de content is_safe y stages. La primera será True o False y la segunda un array con objetos de los
            diferentes verificators.
        """
        raise NotImplementedError()
