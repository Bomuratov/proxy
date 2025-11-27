from pydantic import BaseModel
from typing import Dict

class ResponseModel(BaseModel):
    all_expenses: int
    for_fuel: int
    for_baby: int
    for_communal: int
    for_wifi: int
    for_eats: int
    for_wife: int
    auto_credit: int
    credit: int


class RespModel(BaseModel):
    remainder: int
    all_expenses: int
    expenses_list: ResponseModel
    


class PayloadModel(BaseModel):
    income_wife: int
    income_husband: int
    advance_wife: int
    advance_husband: int
    for_fuel: int
    for_baby: int
    for_communal: int
    for_wifi: int
    for_eats: int
    for_wife: int
    auto_credit: int
    credit: int