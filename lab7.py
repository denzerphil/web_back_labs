from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

films = []

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')