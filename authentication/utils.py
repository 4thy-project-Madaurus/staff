from permit.sync import Permit
from django.conf import settings
from django.apps import apps
from permit.enforcement  import interfaces,enforcer
# Assuming you're accessing this from a module within your Django project
"""
This file contains the utility functions for the authentication app
Do not evener change the app_key, it is used to secure the application
"""



def  create_permit_user(user:dict):
    try:
        permit:Permit = apps.get_app_config('authentication').permit
    except Exception as e:
        print(e)
        return
    try:
    # get the permit from authentication app
        user_data = {
            "key": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
        # run the cooroutine of permit create user and after this correoutine is done, run assign role coroutine
        permit.api.users.create(user_data=user_data)
        permit.api.users.assign_role({
            "user":user_data["key"],
            "role":user["role"],
            "tenant":settings.PERMIT_TENANT
        })
        if user["role"] == "admin":
            permit.api.users.assign_role({
                "user":user_data["key"],
                "role":f"application:{settings.APP_KEY}#Admin",
                "tenant":settings.PERMIT_TENANT
            })
        elif user["role"] == "student":
            try:
                print("Grouping ")
                group_promo = user['group'] + "-" + user['promo']
                promo = user['promo']
                permit.api.resource_instances.create(instance_data={
                        "key": group_promo,
                        "tenant": settings.PERMIT_TENANT,
                        "resource": "group",
                })
                permit.api.users.assign_role({
                    "user":user_data["key"],
                    "role":f"group:{group_promo}#Members",
                    "tenant":settings.PERMIT_TENANT
                })
            except Exception as e:
                print("Error in creating group")
                print(e)
            try:
                print(f"create promo {user['promo']}")
                permit.api.resource_instances.create(instance_data={
                    "key": promo,
                    "tenant": settings.PERMIT_TENANT,
                    "resource": "promo",
                })
                permit.api.users.assign_role({
                    "user": user_data["key"],
                    "role": f"promo:{promo}#Members",
                    "tenant": settings.PERMIT_TENANT
                })
            except Exception as e:
                print("Error in creating Promo")
                print(e)
        else:
            print("Teacher role")
        return
    except Exception as e:
        print("Error in creating permit user")
        print(e)
        return


