from flask import Blueprint, render_template, request, session
from datetime import datetime, timedelta
from db_mamager import getCursor

# create a blueprint
manage_view_subscription_status = Blueprint(
    'manage_view_subscription_status',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# create a route to display the subscription status
@manage_view_subscription_status.route('/')
def get_subscription_status():
    cursor = getCursor()

    # link members, subscription_plans and specific_subscription tables together
    query = '''
    SELECT members.id, members.first_name, members.last_name,
    subscription_plans.type, specific_subscriptions.start_date,
    specific_subscriptions.end_date
    FROM members
    JOIN specific_subscriptions
    ON members.id = specific_subscriptions.user_id
    JOIN subscription_plans
    ON specific_subscriptions.subscription_plan_id = subscription_plans.id
    ORDER BY specific_subscriptions.end_date DESC;
    '''
    cursor.execute(query)

    # fetch all the data
    results = cursor.fetchall()

    # process subscription status
    current_date = datetime.now().date()
    processed_results = []
    for result in results:
        start_date = result[4]
        end_date = result[5]

        if start_date <= current_date <= end_date and end_date - current_date <= timedelta(days=10):
            subscription_status = 'Expiring'
        elif start_date <= current_date <= end_date:
            subscription_status = 'Active'
        
        else:
            subscription_status = 'Expired'

        processed_result = (*result, subscription_status)
        processed_results.append(processed_result)

    return render_template('/manage_view_subscription_status/subscription_status.html', results=processed_results)
