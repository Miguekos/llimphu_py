# backend/tancho/pets/models.py
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional
from pytz import timezone

class Registros(BaseModel):
    """[summary]
        Base pet abstraction model.

    [description]
        Used to abstract out basic pet fields.

    Arguments:
        BaseModel {[type]} -- [description]
    """
    deuda_pendiente_cliente: str
    direccion_cliente: str
    nombre_cliente: str
    # nombre_tipo_de_pago: ""
    # servi_selec: ""
    # service_cliente: ""
    service_pago_del_cliente: str
    # service_restante_cliente: ""
    service_tipo_de_pago: str
    tabla_de_servicios: List[object] = []
    total_a_pagar_cliente: float

    # nombre: str
    # descripcion: str
    # precio: float
    # descuento: float = None
    # activo: str = None
    created_at: datetime = None
    last_modified: datetime = None

    @validator('created_at', pre=True, always=True)
    def default_ts_created(cls, v):
        lima = timezone('America/Lima')
        print(datetime.now(lima))
        return v or datetime.now(lima)

    @validator('last_modified', pre=True, always=True)
    def default_ts_modified(cls, v, *, values, **kwargs):
        return v or values['created_at']


class RegistrosOnDB(Registros):
    """[summary]
    Actual model used at DB level

    [description]
    Extends:
        PetBase
    Adds `_id` field.

    Variables:
        _id: str {[ObjectId]} -- [id at DB]
    """
    id_: str

