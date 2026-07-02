from typing import Generic, TypeVar, Any

L = TypeVar('L')  # Tipo para el Error (Left)
R = TypeVar('R')  # Tipo para el Éxito (Right)

class Either(Generic[L, R]):
    """Clase base abstracta para representar un valor de dos posibles tipos."""
    def is_left(self) -> bool: raise NotImplementedError
    def is_right(self) -> bool: raise NotImplementedError

class Left(Either[L, Any]):
    """Representa el fallo. Típicamente contiene el error o el contexto."""
    def __init__(self, value: L):
        self.value = value
    def is_left(self) -> bool: return True
    def is_right(self) -> bool: return False
    def __repr__(self): return f"Left({self.value!r})"

class Right(Either[Any, R]):
    """Representa el éxito. Contiene el resultado esperado."""
    def __init__(self, value: R):
        self.value = value
    def is_left(self) -> bool: return False
    def is_right(self) -> bool: return True
    def __repr__(self): return f"Right({self.value!r})"