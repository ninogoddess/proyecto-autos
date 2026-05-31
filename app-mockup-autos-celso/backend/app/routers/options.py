"""
Router para el endpoint de opciones del formulario.
Retorna las categorías válidas para cada campo.
"""

from fastapi import APIRouter

from ..services.options import get_options

router = APIRouter(tags=["Opciones"])


@router.get(
    "/options",
    summary="Obtener opciones válidas para el formulario",
    description=(
        "Retorna las opciones válidas para cada campo del formulario de predicción. "
        "Las opciones corresponden a las categorías presentes en el dataset de entrenamiento."
    ),
)
def options() -> dict:
    """Endpoint que expone las opciones válidas del formulario."""
    return get_options()
