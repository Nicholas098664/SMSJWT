from flask import Blueprint, jsonify, request
from services.student_service import addstudent, Allstudents,getstudent,delete,update,getbyname,counter
from auth.token_required import token_required
from admin_required import admin_required
from database import get_db_connection, log_action


student_Tp = Blueprint("student", __name__)

@student_Tp.route("/Allstudents", methods=["GET", "POST"])
@token_required
def students(payload):
    if request.method == "GET":
        students = Allstudents()
        return jsonify(students)

    if request.method == "POST":
        data = request.get_json()
        created = addstudent(data)

        return jsonify({"message": "student added"})

@student_Tp.route("/getstudent/<student_id>", methods = ["GET"]) 
@token_required   
def get_student_route(student_id, payload):
    student = getstudent(student_id)

    if student:
        return jsonify(student)
    return jsonify({
        "message": "student not found"
    }), 404

@student_Tp.route("/update/<student_id>", methods = ["PUT"])
@token_required
@admin_required
def update_student_route(student_id, payload):
    if payload.get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Only admins can upadte students"
        }), 403

    data = request.get_json()
    updated= update(student_id, data)
    
    
    if updated:
           log_action(
        payload["user_id"],
        f"Updated student {data.get('name')}"
    )
           
    return jsonify({
                "success": True,
                "message": "Student updated successfully"
            })
    return  jsonify({
            "success": False,
            "message": " fail to update student "
        })
@student_Tp.route("/delete/<student_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_student_route(student_id, payload):

    if payload.get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Only admins can delete students"
        }), 403

    deleted = delete(student_id)
    
    if deleted:
         log_action(
        payload["user_id"],
        f"Deleted student ID {student_id}"
    )
    return jsonify({
                "success": True,
                "message": "Student deleted successfully"
            })
    return  jsonify({
            "success": False,
            "message": " fail to delete student "
        })

@student_Tp.route("/addstudent", methods = ["POST"])
@token_required
@admin_required
def add_student_route(payload):
    
    if payload.get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Only admins can addstudents"
        }), 403
    data = request.get_json()
    created = addstudent(data)
    log_action(payload["user_id"], f"Added student {data.get('name')}")

    if created:
        return jsonify({
                "success": True,
                "message": "Student added successfully"
            })
    return  jsonify({
            "success": False,
            "message": " fail to add student "
        })

@student_Tp.route("/getbyname", methods = ["GET"])
@token_required
def getbyname_route():
    name = request.args.get(name)
    student = getbyname(name)
    if student:
        return jsonify (student)
    return jsonify({"message":"no student found"})    

@student_Tp.route("/counter", methods=["GET"])
@token_required
def counter_route(payload):
    try:
        count = counter()

        return jsonify({
            "success": True,
            "totalStudent": count
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500