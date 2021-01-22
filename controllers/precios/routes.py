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

from .models import PreciosOnDB, Precios

precios_router = APIRouter()


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


# def fix_id(resp):
#     # print(resp)
#     resp["id_"] = str(resp["_id"])
#     #resp["created_at"] = formatDate(resp["created_at"])
#     #resp["last_modified"] = formatDate(resp["last_modified"])
#     return resp

def fix_id(info):
    print(info)
    info["id_"] = str(info["_id"])
    info.pop("_id")
    return info


@precios_router.get("/")
async def get_precios():
    try:
        total = []
        resp = DB.precios.find({}).sort('_id', -1)
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


@precios_router.get("/{id}")
async def get_precios_id(id):
    try:
        print(id)
        global total
        total = []
        # registro = await DB.precios.find({"servicio_id": "{}".format(id)})
        registro = DB.precios.find({"servicio_id": "{}".format(id)})
        return list(map(fix_id, await registro.to_list(length=100)))
        # if registro:
        #     print(registro)
        #     # registro["id_"] = str(registro["_id"])
        #     for x in registro:
        #         x.pop('_id')
        #         total.append(x)
        #     # registro["created_at"] = formatDate(registro["created_at"])
        #     # registro["last_modified"] = formatDate(registro["last_modified"])
        #     return total
    except:
        raise HTTPException(status_code=404, detail="not found")


@precios_router.post("/")
async def add_precios(price: Precios):
    try:
        # print("precios", price)
        price = price.dict()
        print(price)
        resp = await DB.precios.insert_one(price)
        return {
            "id": str(resp.inserted_id)
        }
    except NameError:
        print(NameError)


@precios_router.put("/")
async def update_precios():
    return {"result": "precios"}


@precios_router.delete("/")
async def delete_precios():
    return {"result": "precios"}
