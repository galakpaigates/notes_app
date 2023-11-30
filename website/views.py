from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def index():
    
    if request.method == "POST":
        
        note = request.form.get('note')
        
        if len(note) < 2:
            flash(message="Note must be atleast 2 characters!", category='error')
        
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            current_user.is_authenticated = True
            flash(message="Note added!", category='success')
            
    return render_template("index.html", user=current_user)
    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

