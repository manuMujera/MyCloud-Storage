from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key" 


STORAGE_FILE = 'files.json'

def get_files():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_files(files):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(files, f, indent=2)

@app.route('/')
def index():
    files = get_files()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filename = request.form.get('filename')
        
        if not filename:
            flash('Please enter a filename', 'danger')
            return redirect(url_for('upload'))
            
        files = get_files()
        
        if any(file['name'] == filename for file in files):
            flash('A file with this name already exists', 'danger')
            return redirect(url_for('upload'))
            
        # Add new file
        files.append({
            'name': filename,
            'size': '1 MB',  # Simulated size
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'id': len(files) + 1
        })
        
        save_files(files)
        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('upload.html')

@app.route('/update/<int:file_id>', methods=['GET', 'POST'])
def update(file_id):
    files = get_files()
    
    file = next((f for f in files if f['id'] == file_id), None)
    
    if not file:
        flash('File not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_filename = request.form.get('filename')
        
        if not new_filename:
            flash('Please enter a filename', 'danger')
            return redirect(url_for('update', file_id=file_id))
            
      
        if any(f['name'] == new_filename and f['id'] != file_id for f in files):
            flash('A file with this name already exists', 'danger')
            return redirect(url_for('update', file_id=file_id))
            
        # Update file
        file['name'] = new_filename
        save_files(files)
        
        flash(f'File updated successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('update.html', file=file)

@app.route('/delete/<int:file_id>')
def delete(file_id):
    files = get_files()
    
    file = next((f for f in files if f['id'] == file_id), None)
    
    if not file:
        flash('File not found', 'danger')
    else:
        # Remove the file
        files = [f for f in files if f['id'] != file_id]
        save_files(files)
        flash('File deleted successfully!', 'success')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)