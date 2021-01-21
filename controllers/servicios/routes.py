# backend/tancho/pets/routes.py
import shutil
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from bson.objectid import ObjectId
from config.config import DB, CONF
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
import logging
from fastapi.responses import FileResponse

from .models import ServiciosOnDB, Servicios

servicios_router = APIRouter()


def validate_object_id(id_: str):
    try:
        _id = ObjectId(id_)
    except Exception:
        if CONF["fastapi"].get("debug", False):
            logging.warning("Invalid Object ID")
        raise HTTPException(status_code=400)
    return _id


async def _get_user_or_404(id_: str):
    _id = validate_object_id(id_)
    pet = await DB.users.find_one({"_id": _id})
    if pet:
        return fix_pet_id(pet)
    else:
        raise HTTPException(status_code=404, detail="Pet not found")


def fix_id(info):
    info["id_"] = str(info["_id"])
    info.pop("_id")
    return info


@servicios_router.get("/")
async def get_servicios():
    try:
        total = []
        resp = DB.servicios.find({}).sort('_id', -1)
        docs = await resp.to_list(None)
        for x in docs:
            # print(x)
            total.append(fix_id(x))
        # print(docs)
        # while docs:
        #     print(docs)
        #     docs = await resp.to_list(length=2)
        return {"result": total}
    except:
        raise HTTPException(status_code=404, detail="Error controlado")


@servicios_router.post("/")
async def add_servicios(service: Servicios):
    try:
        # print("servicios", service)
        service = service.dict()
        resp = await DB.servicios.insert_one(service)
        return {
            "id": str(resp.inserted_id),
            "registro": service['nombre']
        }
    except NameError:
        print(NameError)


@servicios_router.put("/")
async def update_servicios():
    return {"result": "servicios"}


@servicios_router.delete("/")
async def delete_servicios():
    return {"result": "servicios"}
