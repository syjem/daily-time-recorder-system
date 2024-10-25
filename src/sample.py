
# import sqlite3
# from flask import g, request, session, jsonify, render_template

# # Database connection
# DATABASE = 'sample.db'


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


# @app.route('/sample', methods=['GET', 'POST'])
# def sample():
#     if request.method == 'POST':
#         data = request.get_json()
#         user_id = session.get('user_id', 1)

#         with get_db() as conn:
#             for schedule in data:
#                 day = schedule['day']
#                 day_off = schedule['day_off']
#                 start_time = schedule.get('start_time', None)
#                 end_time = schedule.get('end_time', None)

#                 conn.execute('''
#                     CREATE TABLE IF NOT EXISTS schedules (
#                         id INTEGER PRIMARY KEY,
#                         user_id TEXT NOT NULL,
#                         day TEXT CHECK(day IN ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')) NOT NULL,
#                         day_off BOOLEAN NOT NULL,
#                         start_time TIME,
#                         end_time TIME,
#                         UNIQUE(user_id, day),
#                         FOREIGN KEY(user_id) REFERENCES users(id)
#                     );
#                 ''')
#                 conn.commit()

#                 conn.execute(
#                     '''
#                     INSERT INTO schedules (user_id, day, day_off, start_time, end_time)
#                     VALUES (?, ?, ?, ?, ?)
#                     ON CONFLICT(user_id, day)
#                         DO UPDATE SET day_off = excluded.day_off, start_time = excluded.start_time, end_time = excluded.end_time;
#                     ''',
#                     (user_id, day, day_off, start_time, end_time)
#                 )

#                 conn.commit()

#         return jsonify({'message': 'Schedules updated successfully!'})

#     return render_template("time-schedule.html")


# @app.route("/forgot-password", methods=['GET', 'POST'])
# @logout_required
# def forgot_password():
#     return render_template("forgot-password.html")


# @app.route('/terms-and-conditions')
# def terms_and_conditions():
#     return render_template("terms-and-conditions.html")
