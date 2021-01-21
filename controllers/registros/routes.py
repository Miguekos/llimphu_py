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

from .models import RegistrosOnDB, Registros

registros_router = APIRouter()


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
        return fix_id(pet)
    else:
        raise HTTPException(status_code=404, detail="Pet not found")


def fix_id(info):
    info["id_"] = str(info["_id"])
    info.pop("_id")
    return info


@registros_router.get("/")
async def get_registros():
    try:
        total = []
        resp = DB.registros.find({}).sort('_id', -1)
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


@registros_router.post("/")
async def add_registros(register: Registros):
    try:
        # print("registros", register)
        register = register.dict()
        print(register)
        resp = await DB.registros.insert_one(register)
        return {
            "id": str(resp.inserted_id),
            "registro": register['nombre_cliente']
        }
    except NameError:
        print(NameError)


@registros_router.put("/")
async def update_registros():
    return {"result": "registros"}


@registros_router.delete("/")
async def delete_registros():
    return {"result": "registros"}
