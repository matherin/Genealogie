# from flask import jsonify
# from ..datamodels import *
# from datetime import datetime
# from .contracts_service import get_group_by_id, get_location_by_id
# from sqlalchemy import extract



# def get_user_invoice(year, month, id):
#     """
#     get_group_invoice returns the abrechnung of a group on the given month

#     if the year or month is invalid, it returns 400
#     if group id does not exist, it returns 404

#     {
#       "rot":403,
#       "blau":432,
#       "salat":345,
#       "orders": [
#         {
#           "date": "2025-02-01",
#           "order": ["rot", "salad"]
#         },
#         ...
#       ]
#     }
#     """
#     date_str = f"{year}-{month}"
#     try:
#         _ = datetime.strptime(date_str, '%Y-%m').date()
#     except ValueError:
#         return jsonify({"error": "Provided date is invalid. Use /YYYY/MM "}), 400
#     res = {}
#     res['blau'] = 0
#     res['rot'] = 0
#     res['salad'] = 0
#     res['orders'] = []
#     meal_map = {
#         1: ['rot'],
#         2: ['blau'],
#         3: ['salad'],
#         4: ['rot', 'salad'],
#         5: ['blau', 'salad'],
#         6: []
#     }

#     orders = dict()
#     user_orders = AccountOrder.query.filter(AccountOrder.account_id == id).all()
#     users_group_orders = set()

#     for o in user_orders:
#         users_group_orders.add(o.group_order_id)

#     for o in users_group_orders:
#         group_order = GroupOrder.query.filter(o == GroupOrder.id).first()

#         # check if date matches
#         if group_order.date.strftime("%Y-%m") != date_str:
#             continue

#         # get orders of user
        
#         for go in group_order.content:
#             if int(go.account_id) != int(id):
#                 continue

#             if group_order.date.strftime("%Y-%m-%d") not in orders:
#                 orders[group_order.date.strftime("%Y-%m-%d")] = dict()
#                 orders[group_order.date.strftime("%Y-%m-%d")]["order"] = set()
#                 orders[group_order.date.strftime("%Y-%m-%d")]["date"] = group_order.date.strftime("%Y-%m-%d")


#             food_order = meal_map.get(go.meal_id)
#             for fo in food_order:
#                 orders[group_order.date.strftime("%Y-%m-%d")]["order"].add(fo)
#                 res[fo] += 1 



#     # fill orders map
#     for d,v in orders.items():
#         v['order']=list(v['order'])
#         res['orders'].append(v)

#     res['orders']=list(res['orders'])
#     return jsonify(res), 200


# def get_location_invoice(year, month, id):
#     """
#     get_group_invoice returns the abrechnung of a group on the given month

#     if the year or month is invalid, it returns 400
#     if group id does not exist, it returns 404

#     {
#       "rot":403,
#       "blau":432,
#       "salat":345,
#       "orders": [
#         {
#           "group": "1",
#           "rot": 15,
#           "blau":12,
#           "salat":13
#         },
#         ...
#       ]
#     }
#     """
#     date_str = f"{year}-{month}"
#     try:
#         _ = datetime.strptime(date_str, '%Y-%m').date()
#     except ValueError:
#         return jsonify({"error": "Provided date is invalid. Use /YYYY/MM "}), 400

#     # get groups of location 
#     l = get_location_by_id(id)
#     if not l:
#         return jsonify({"error": "Group not found"}), 404

#     res = {}
#     res['blau'] = 0
#     res['rot'] = 0
#     res['salad'] = 0
#     res['orders'] = []

#     for g in l.groups:
#         (abr, s) = get_group_invoice(year, month, g.id)
#         if s != 200:
#             continue
#         d = abr.json

#         if 'blau' in d:
#             res['blau'] += d['blau']
#         if 'rot' in d:
#             res['rot'] += d['rot']
#         if 'salad' in d:
#             res['salad'] += d['salad']

#         res['orders'].append({
#             "blau":d["blau"] if "blau" in d else 0 ,
#             "rot":d["rot"] if "rot" in d else 0 ,
#             "salad":d["salad"] if "salad" in d else 0 ,
#             "group": g.id
#             })


#     return jsonify(res), 200


# def get_group_invoice(year, month, id): 
#     """
#     get_group_invoice returns the abrechnung of a group on the given month

#     if the year or month is invalid, it returns 400
#     if group id does not exist, it returns 404

#     {
#       "rot":403,
#       "blau":432,
#       "salat":345,
#       "orders": [
#         {
#           "user": "1",
#           "rot": 15,
#           "blau":12,
#           "salat":13
#         },
#         ...
#       ]
#     }
#     """
#     date_str = f"{year}-{month}"
#     try:
#         _ = datetime.strptime(date_str, '%Y-%m').date()
#     except ValueError:
#         return jsonify({"error": "Provided date is invalid. Use /YYYY/MM "}), 400


#     # get group's orders
#     group = get_group_by_id(id)
#     if not group:
#         return jsonify({"error": "Group not found"}), 404

#     res = dict()
#     res['blau'] = 0
#     res['rot'] = 0
#     res['salad'] = 0
#     meal_map = {
#         1: ['rot'],
#         2: ['blau'],
#         3: ['salad'],
#         4: ['rot', 'salad'],
#         5: ['blau', 'salad'],
#         6: []
#     }

#     users = []

    
#     for g in group.group_orders:
#         # check if date matches
#         if g.date.strftime("%Y-%m") != date_str:
#             continue
        
#         # iterate over individual account orders
#         for c in g.content:
#             mm = meal_map.get(c.meal_id)
#             for m in mm:
#                 if m not in res:
#                     res[m] = 0
#                 res[m] += 1

#                 check = False
#                 for uu in users:
#                     if uu['user'] == c.account_id:
#                         if m not in uu:
#                             uu[m] = 0
#                         uu[m] += 1
#                         check = True

#                 if not check:
#                     u = {"user":c.account_id}
#                     u[m] = 1
#                     users.append(u)
#     res["orders"] = users
#     return jsonify(res), 200
        
