from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from bloom.models.portfolio import Portfolio
from bloom.utils.rapid_api import get_mutual_fund_data, get_fund_houses, get_fund
from bloom import db, scheduler, create_app
from datetime import datetime, timezone

bp = Blueprint('portfolio', __name__)


@bp.route("/home", methods=["GET", "POST"])
@bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    all_funds = get_mutual_fund_data()

    # Search
    fund_families = get_fund_houses(all_funds)
    selected_family = request.form.get("fund_family", None)
    if selected_family:
        all_funds = get_mutual_fund_data(Scheme_Type="Open", AMC_Code=selected_family)
        all_funds = [fund for fund in all_funds if fund["AMC_Code"] == selected_family]

    # Pagination logic
    start = (page - 1) * per_page
    end = start + per_page
    paginated_funds = all_funds[start:end]

    # Calculate total pages for pagination controls
    total_funds = len(all_funds)
    total_pages = (total_funds // per_page) + (1 if total_funds % per_page > 0 else 0)

    print(f"Displaying page {page} of {total_pages} with {len(paginated_funds)} items")

    return render_template(
        "portfolio/home.html",
        all_funds=paginated_funds,
        page=page,
        total_pages=total_pages,
        fund_families=fund_families
    )

# @bp.route("/data")
# @login_required
# def get_data():
#     all_funds = get_mutual_fund_data()
#     print(f"All funds:\n{all_funds[:15]}\n\n")
#     return jsonify(all_funds[:15])

@bp.route("/fund_portfolio/<name>")
@login_required
def fund_portfolio(name):
    id = request.args.get("fund_id")
    fund_data = get_fund(int(id))
    if not fund_data:
        fund_data = {"error": "No Data Available!!!"}
    return render_template('portfolio/fund_portfolio.html', name=name, fund_data=fund_data)

@bp.route("/explore")
@login_required
def explore():
    return render_template("portfolio/explore.html")

@bp.route('/portfolio')
@login_required
def profile():
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio/portfolio.html', portfolios=portfolios)


@bp.route('/fund-selector')
@login_required
def fund_selector():
    fund_houses = get_fund_houses()
    return render_template('portfolio/fund_selector.html', fund_houses=fund_houses)

# @bp.route('/transact/<int:fund_id>', methods=["GET", "POST"])
# @login_required
# def transact(fund_id):
#     fund_data = get_fund(id)
#     return jsonify(fund_data)
#     # return render_template('portfolio/fund_selector.html', fund_houses=fund_houses)

@bp.route('/transact/<int:fund_id>', methods=["GET", "POST"])
@login_required
def transact(fund_id):
    # Fetch the fund data based on fund_id
    fund_data = get_fund(fund_id)

    if not fund_data:
        return jsonify({"error": "Fund data not found"}), 404

    # Check if form is submitted to buy or sell
    if request.method == "POST":
        action = request.form.get("action")  # Get 'buy' or 'sell' action
        units = float(request.form.get("units"))  # Get the number of units to buy/sell

        # Get the current user's portfolio to check if they already have the fund
        portfolio = Portfolio.query.filter_by(user_id=current_user.id, scheme_code=fund_data['Scheme_Code']).first()

        if action == "buy":
            if portfolio:
                # If user already has this fund, update the units and value
                portfolio.units += units
            else:
                # If user doesn't have this fund, create a new portfolio entry
                current_value = units * float(fund_data['Face_Value'])
                portfolio = Portfolio(
                    user_id=current_user.id,
                    fund_name=fund_data['Scheme_Name'],
                    scheme_code=fund_data['Scheme_Code'],
                    units_owned=units,
                    purchase_price=fund_data["Face_Value"],
                    investment_amount=current_value,
                    current_value=current_value
                )
                db.session.add(portfolio)

        elif action == "sell":
            if portfolio and portfolio.units >= units:
                # If user has enough units, update the portfolio by reducing the units
                portfolio.units -= units
                # Recalculate the current value after selling
                current_value = portfolio.units * float(fund_data['Face_Value'])
                portfolio.current_value = current_value
                if portfolio.units == 0:
                    db.session.delete(portfolio)  # If units become zero, delete the portfolio entry
            else:
                return jsonify({"error": "Insufficient units to sell"}), 400

        # Commit the changes to the database
        db.session.commit()

        # Redirect user to the portfolio page or show a success message
        return redirect(url_for('portfolio.profile'))

    # If the request method is GET, just return the fund data to display
    return render_template('portfolio/fund_portfolio.html', name=fund_data['Scheme_Name'], fund_data=fund_data)

@bp.route('/add-investment', methods=['POST'])
@login_required
def add_investment():
    fund_house = request.form.get('fund_house')
    scheme_code = request.form.get('scheme_code')
    units = float(request.form.get('units'))

    fund_data = get_mutual_fund_data(Scheme_Code=scheme_code)
    current_value = units * float(fund_data['Face_Value'])

    portfolio = Portfolio(
        user_id=current_user.id,
        fund_house=fund_house,
        scheme_code=scheme_code,
        units=units,
        current_value=current_value
    )

    db.session.add(portfolio)
    db.session.commit()

    return redirect(url_for('portfolio.profile'))


def update_portfolio_values():
    app = create_app()
    with app.app_context():
        portfolios = Portfolio.query.all()
        print(f"Portfolios:\n {portfolios[0]}\n\n")
        for portfolio in portfolios:
            print(f"Portfolio: {portfolio}")
            fund_data = get_mutual_fund_data(Scheme_Code=portfolio.Scheme_Code)
            portfolio.current_value = portfolio.units * float(fund_data["Face_Value"])
            portfolio.last_updated = datetime.now(timezone.utc)
        db.session.commit()


# Schedule portfolio update every hour
scheduler.add_job(
    func=update_portfolio_values,
    trigger="interval",
    minutes=1
)

# scheduler.add_job(
#     func=update_portfolio_values,
#     trigger="interval",
#     # hours=1
# )