from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.address_model import Address as AddressModel
from models.user_model import Users as UserModel
from schemas.address_schema import Address as AddressSchema
from utils.util import create_db_session, get_current_user, notfound_exception

router = APIRouter(
    prefix="/api/address",
    tags=["Address Management"],
    responses={401: {"detail": "Not authorized"}},
)

db_dependency = Annotated[Session, Depends(create_db_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/")
async def create_address(
    address: AddressSchema,
    user: user_dependency,
    db: db_dependency,
):
    if user is None:
        raise notfound_exception("User")
    address_model = address_model()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()

    user_model = db.query(UserModel).filter(UserModel.user_id == user.get("id")).first()

    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()
