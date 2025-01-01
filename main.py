from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
import folium
import re

app = Flask(__name__)
app.secret_key = "secret"
# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Making the table
class cafe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    map_url: Mapped[str] = mapped_column()
    img_url: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean)
    has_toilet: Mapped[bool] = mapped_column(Boolean)
    has_wifi: Mapped[bool] = mapped_column(Boolean)
    can_take_calls: Mapped[bool] = mapped_column(Boolean)
    seats: Mapped[str] = mapped_column(String(10), nullable=False)
    coffee_price: Mapped[str] = mapped_column(nullable=False)


@app.route("/")
def home():
    all_cafes = db.session.query(cafe).all()
    return render_template("index.html", all_cafes=all_cafes)


@app.route("/map")
def test():
    cafe_coords = [51.5041961, -0.0874412]
    m = folium.Map(cafe_coords, zoom_start=20)

    folium.Marker(
        location=cafe_coords).add_to(m)
    m.save("templates/map.html")
    return render_template("map.html")


@app.route("/page")
def page():
    id_value = request.args.get("cafe_id")
    cafe_id = cafe.query.get(id_value)
    sockets = cafe_id.has_sockets
    if sockets:
        sockets = "Yes"
    else:
        sockets = "No"
    toilet = cafe_id.has_toilet
    if toilet:
        toilet = "Yes"
    else:
        toilet = "No"
    wifi = cafe_id.has_wifi
    if wifi:
        wifi = "Yes"
    else:
        wifi = "No"
    call = cafe_id.can_take_calls
    if call:
        call = "Yes"
    else:
        call = "No"
    # Making the map
    map_url = request.args.get("map_url")
    pattern = r"(-?\d+\.\d+),(-?\d+\.\d+)"
    match = re.search(pattern, map_url)
    if match:
        lat, lng = map(float, match.groups())
    else:
        raise ValueError("Couldn't extract lat and lng")
    # Using folium
    create_map = folium.Map(location=[lat, lng], zoom_start=20)
    folium.Marker(location=[lat, lng]).add_to(create_map)
    map_html = create_map._repr_html_()
    return render_template("page.html",map_html=map_html, cafe_id=cafe_id,sockets=sockets,toilet=toilet,wifi=wifi,call=call)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            image = request.form.get("image")
            map_url = request.form.get("map_url")
            location = request.form.get("location")
            sockets = request.form.get("socket")
            sockets = sockets == "true"
            toilet = request.form.get("toilet")
            toilet = toilet == "true"
            wifi = request.form.get("wifi")
            wifi = wifi == "true"
            call = request.form.get("call")
            call = call == "true"
            seat = request.form.get("seat")
            price = request.form.get("price")
            new_cafe = cafe(
                name=name,
                map_url=map_url,
                img_url=image,
                location=location,
                has_sockets=sockets,
                has_toilet=toilet,
                has_wifi=wifi,
                can_take_calls=call,
                seats=seat,
                coffee_price=price, )
            db.session.add(new_cafe)
            db.session.commit()
            flash("Added successfully","success")
            return redirect("/")
    except:
        flash("Information already exists","error")
        return redirect("/add")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
