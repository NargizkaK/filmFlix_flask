from flask import Flask, render_template, url_for, request, redirect, abort
import sqlite3 as sql


app = Flask( __name__ )



def fl_access():
    try:
        with sql.connect('filmflix.db') as flConnect:
            # flCursor = flConnect.cursor() #cursor function is used to call the execute method
            flConnect.row_factory = sql.Row
            return flConnect
    
    except sql.OperationalError as e:   # raise sqlerror
        #use the errorr raised to handle the exeption/error
        print(f"Connection failed: {e}")
        
    except sql.ProgrammingError as pe:
        print(f"Not working because: {pe}")
   
    except sql.Error as er:
        print(f"This error: {er}")
   

def get_film(film_id):
    conn = fl_access()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',(film_id,)).fetchone()
    conn.close()
    if film is None:
        abort(404)
    return film

@app.route('/')
def index():
    conn = fl_access() # in ternal con
    films = conn.execute('SELECT * FROM tblFilms ').fetchall()
    return render_template('index.html', title='Home', films=films)

@app.route('/add_film', methods= {'GET','POST'})
def add():
    if request.method == 'POST':
        film = {
            "filmID":request.form.get('filmID'),
            "title":request.form['title'],
            "year":request.form['year'],
            "rating":request.form['rating'],
            "duration":request.form['duration'],
            "genre":request.form['genre']
            
        }
        conn = fl_access()
        conn.execute("INSERT INTO tblFilms (filmID, title, yearReleased, rating, duration, genre) VALUES(:filmID, :title, :year, :rating, :duration, :genre)", film)
    
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/update/<int:film_id>', methods = ('GET', 'POST'))
def update(film_id):
    film = get_film(film_id)
    if request.method == 'POST':
        film = {
            "filmID": film_id,
            "title":request.form.get('title'),
            "year":request.form['year'],
            "rating":request.form['rating'],
            "duration":request.form['duration'],
            "genre":request.form['genre']                    
        }
        
        conn = fl_access()    
        conn.execute(f"UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ? WHERE filmID= ?", (film['title'], film['year'], film['rating'], film['duration'], film['genre'], film['filmID']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('update.html', film = film)



@app.route('/<int:film_id>/delete', methods=('POST',))
def delete(film_id):
    # film=get_film(film_id)
    print(type(film_id))
    conn=fl_access() 
    conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (film_id,))    
    conn.commit()    
    conn.close()   
    return redirect(url_for('index'))
#  return render_template('update.html', film = film)

    



"""
def open_file(file_path): #file_path is the parameter or value
    try:
        with open(file_path) as read_file:
            # read() reads the file content and save it in the variable called rf
            of = read_file.read()
 
            return of
    except FileNotFoundError as nf:
        print(f"File not found: {nf}")
 
def films_menu():
    try:
        option = 0 
        optionsList = ["1","2","3","4","5","6"]
 
        menu_choices = open_file("flmMenutxt")
 
        while option not in optionsList:
            print(menu_choices)
 
            option = input("Enter an option from the menu above (Example: 1 or 3 or 5,,): ")
 
          
            if option not in optionsList:
                print(f"{option} is not a valid choice")
        return option
    except FileNotFoundError as e:
        print(f"Add error: {e}")
        
 
 
mainProgram = True 
 
while mainProgram:
    main_menu = films_menu()
 
    if main_menu == "1":
        printflm.print_films()
    elif main_menu == "2":
        addflmData.add_film()
    elif main_menu == "3":
        amendflm.update_films()
    elif main_menu == "4":
        deleteflm.delete_films()
    elif main_menu == "5":
        searchflm.search_film()
 
    else: 
        mainProgram = False
input("Press Enter to exit....")
 
"""
if __name__ == "__main__":
    app.run(debug=True)