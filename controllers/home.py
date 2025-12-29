from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def about():
    team = [
        {
            "name": "Lathifatul Maulida",
            "nim": "2311082022",
            "role": "Project Manager",
            "photos": [
                "/static/images/team/lathi1.png",
                "/static/images/team/lathi2.png",
                "/static/images/team/lathi3.png",
            ]
        }
        ,{
            "name": "Andini Zakira",
            "nim": "2311081005",
            "role": "Data Analyst",
            "photos": [
                "/static/images/team/andini1.png",
                "/static/images/team/andini2.png",
                "/static/images/team/andini3.png",
            ]
        },
        {
            "name": "Muhammad Dafa Aziul Ardi",
            "nim": "2311082027",
            "role": "Programer",
            "photos": [
                "/static/images/team/dafa1.png",
                "/static/images/team/dafa2.png",
                "/static/images/team/dafa3.png",
            ]
        }
    ]

    return render_template("home/index.html", team=team)