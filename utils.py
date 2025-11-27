
# @router.post("", response_model=RespModel)
# async def calculator(payload: PayloadModel):
    
#     income = (
#         payload.income_husband
#         + payload.income_wife
#         + payload.advance_husband
#         + payload.advance_wife
#     )

#     expanses = (
#         payload.for_fuel
#         + payload.for_baby
#         + payload.for_communal
#         + payload.for_eats
#         + payload.for_wife
#         + payload.for_wifi
#         + payload.auto_credit
#         + payload.credit
#     )
#     result = income - expanses

#     return RespModel(
#         all_expenses=expanses,
#         remainder=result,
#         expenses_list=ResponseModel(
#             all_expenses=expanses,
#             for_fuel=payload.for_fuel,
#             for_baby=payload.for_baby,
#             for_communal=payload.for_communal,
#             for_wifi=payload.for_wifi,
#             for_eats=payload.for_eats,
#             for_wife=payload.for_wife,
#             auto_credit=payload.auto_credit,
#             credit=payload.credit
#         )
#     )