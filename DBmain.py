from flask import Flask, render_template, request
from DBcm import UseDatabase

app = Flask(__name__)
app.config['mydbconf'] = {'host': '127.0.0.1', 'user': 'root',
                          'password': 'password', 'database': 'dbcoursework', }


@app.route('/search', methods=['post'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    title = 'Результат поиска по табельному номеру:'
    with UseDatabase(app.config['mydbconf']) as cursor:
        _SQL = "SELECT table_number," \
               "last_name," \
               "first_name, " \
               "patronymic, " \
               "status," \
               "science_degree," \
               "science_rank," \
               "work_exp, " \
               "code FROM tutor WHERE table_number = '" + phrase + "'"
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Табельный номер',
              'Фамилия',
              'Имя',
              'Отчество',
              'Должность',
              'Научная степень',
              'Научный ранг',
              'Опыт работы',
              'Код кафедры')
    return render_template('result.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/search_by_cathedra_code', methods=['post'])
def do_search_by_cathedra_code() -> 'html':
    phrase = request.form['phrase']
    title = 'Результат поиска по коду кафедры:'
    with UseDatabase(app.config['mydbconf']) as cursor:
        _SQL = "SELECT table_number," \
               "last_name," \
               "first_name, " \
               "patronymic, " \
               "status," \
               "science_degree," \
               "science_rank," \
               "work_exp, " \
               "code FROM tutor WHERE code = '" + phrase + "'"
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Табельный номер',
              'Фамилия',
              'Имя',
              'Отчество',
              'Должность',
              'Научная степень',
              'Научный ранг',
              'Опыт работы',
              'Код кафедры')
    return render_template('result.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/viewthecathedra', methods=['post'])
def view_the_cathedra() -> 'html':
    with UseDatabase(app.config['mydbconf']) as cursor:
        _SQL = """SELECT code, 
                         name_of_cathedra, 
                         dir_last_name, 
                         dir_first_name, 
                         dir_patronymic_name, 
                         priznak_vypuskayushey FROM cathedra ORDER BY code"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Код', 'Название кафедры', 'Фамилия', 'Имя', 'Отчество', 'Признак выпускающей')
    return render_template('result.html',
                           the_title='Список кафедр отсортированный по коду:',
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/viewall', methods=['post'])
def view_all() -> 'html':
    with UseDatabase(app.config['mydbconf']) as cursor:
        _SQL = "select code, " \
               "last_name, " \
               "first_name, " \
               "patronymic, " \
               "cathedra.name_of_cathedra " \
               "from tutor left join cathedra using (code) order by code;"
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Код кафедры',
              'Фамилия преподавателя',
              'Имя преподавателя',
              "Отчество преподавателя",
              'Название кафедры')
    return render_template('result.html',
                           the_title='Все преподаватели',
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/viewcount', methods=['post'])
def view_count() -> 'html':
    with UseDatabase(app.config['mydbconf']) as cursor:
        _SQL = "select cathedra.code, " \
               "name_of_cathedra, " \
               "count(tutor.code) " \
               "from cathedra inner join tutor on " \
               "cathedra.code=tutor.code group by cathedra.code order by code;"
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Код кафедры',
              'Название кафедры', 'Количество преподавателей')
    return render_template('result.html',
                           the_title='Количество преподавателей на каждой кафедре',
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title="Курсовая работа")


app.run(debug=True)
