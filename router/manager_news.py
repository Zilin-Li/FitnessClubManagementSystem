from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
import datetime


# create a blueprint
manager_news = Blueprint(
    'manager_news',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# create a route to display the news
@manager_news.route('/')
def show_manager_news():
    title = request.args.get('title')
    publish_time = request.args.get('publish_time')

    # Build the query with placeholders
    query = """
        SELECT
            id,
            title,
            content,
            published_at,
            modified_at,
            manager_id
        FROM news
        WHERE 1=1
    """

    params = []

    if title:
        query += " AND title LIKE %s"
        # Append '%' before and after the title to perform a fuzzy search
        params.append(f"%{title}%")

    if publish_time:
        try:
            publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d")
            query += " AND DATE(published_at) = %s"
            params.append(publish_time)
        except ValueError:
            pass  # Handle invalid date format

    query += " ORDER BY published_at DESC"

    dbconn = getCursor()
    try:
        dbconn.execute(query, params)
        news = dbconn.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        news = None

    # Check if publish_time is set and there are no news available
    if publish_time and not news:
        flash("No news available for the selected date.", "error")
        return render_template('/manager_view_news/show_news.html', news=news)

    # Check if there are no news for the selected title
    if not news and title:
        flash("No news found for the specified title.", "error")

    return render_template('/manager_view_news/show_news.html', news=news)


# create a route to add news
@manager_news.route('/add_news', methods=['GET', 'POST'])
def manager_add_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title is not None and content is not None:
            try:
                manager_id = session.get('user_id')
                print(manager_id)
                if manager_id is None:
                    flash('User session not set. Please log in again.', 'danger')
                    # or any other appropriate action
                    return redirect(url_for('login'))

                cursor = getCursor()
                cursor.execute("""
                    INSERT INTO news (title, content, manager_id)
                    VALUES (%s, %s, %s)
                """, (title, content, manager_id))
                flash('News added successfully', 'success')
                return redirect(url_for('manager_news.show_manager_news'))

            except Exception as e:
                print(f"An error occurred: {e}")
                flash('An error occurred, please try again', 'danger')
        else:
            flash('Please fill all the form', 'danger')

    return render_template('/manager_view_news/add_news.html')


# create a route to show indevidual news
@manager_news.route('/<int:news_id>')
def show_indevidual_news(news_id):
    query = """
        SELECT
            id,
            title,
            content,
            published_at,
            modified_at,
            manager_id
        FROM news
        WHERE id = %s
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query, (news_id,))
        news = dbconn.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
        news = None

    return render_template('/manager_view_news/show_indevidual_news.html', news=news)


# create a route to delete news
@manager_news.route('/delete_news/<int:news_id>')
def delete_news(news_id):
    try:
        cursor = getCursor()
        cursor.execute("""
            DELETE FROM news
            WHERE id = %s
        """, (news_id,))
        flash('News deleted successfully', 'success')
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred, please try again', 'danger')

    return redirect(url_for('manager_news.show_manager_news'))


# create a route to edit news
@manager_news.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    query = """
        SELECT
            id,
            title,
            content,
            published_at,
            modified_at,
            manager_id
        FROM news
        WHERE id = %s
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query, (news_id,))
        news = dbconn.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
        news = None

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if title is not None and content is not None:
            try:
                manager_id = session.get('user_id')
                if manager_id is None:
                    flash('User session not set. Please log in again.', 'danger')
                    # or any other appropriate action
                    return redirect(url_for('login'))

                cursor = getCursor()
                cursor.execute("""
                    UPDATE news
                    SET title = %s, content = %s
                    WHERE id = %s
                """, (title, content, news_id))
                flash('News updated successfully', 'success')
                return redirect(url_for('manager_news.show_manager_news'))

            except Exception as e:
                print(f"An error occurred: {e}")
                flash('An error occurred, please try again', 'danger')
        else:
            flash('Please fill all the form', 'danger')

    return render_template('/manager_view_news/edit_news.html', news=news)
