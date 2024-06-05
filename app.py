from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

participants = []
bets = {}
amounts = {}
actual_finish_order = {
    "Mountain 1": ["Alice", "Bob", "Charlie", "Dave"],
    "Mountain 2": ["Charlie", "Alice", "Dave", "Bob"],
    "Mountain 3": ["Bob", "Charlie", "Alice", "Dave"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_participant', methods=['POST'])
def add_participant():
    name = request.form['name']
    mountain1 = request.form['mountain1']
    mountain2 = request.form['mountain2']
    mountain3 = request.form['mountain3']
    amount = request.form['amount']

    if name and mountain1 and mountain2 and mountain3 and amount:
        participants.append(name)
        bets[name] = [mountain1, mountain2, mountain3]
        amounts[name] = float(amount)

    return redirect(url_for('index'))

@app.route('/participants')
def show_participants():
    return render_template('participants.html', participants=participants, amounts=amounts)

@app.route('/set_finish_order', methods=['GET', 'POST'])
def set_finish_order():
    global actual_finish_order  # Declare as global to modify the dictionary

    if request.method == 'POST':
        actual_finish_order['Mountain 1'] = request.form.getlist('mountain1')
        actual_finish_order['Mountain 2'] = request.form.getlist('mountain2')
        actual_finish_order['Mountain 3'] = request.form.getlist('mountain3')
        return redirect(url_for('index'))

    return render_template('set_finish_order.html', actual_finish_order=actual_finish_order)

@app.route('/calculate_results')
def calculate_results():
    global bets, amounts  # Declare as global to avoid UnboundLocalError

    points = {}

    for participant, bet in bets.items():
        points[participant] = 0
        for i, mountain in enumerate(["Mountain 1", "Mountain 2", "Mountain 3"]):
            if bet[i] == actual_finish_order[mountain][0]:
                points[participant] += 10
            elif bet[i] == actual_finish_order[mountain][1]:
                points[participant] += 7
            elif bet[i] == actual_finish_order[mountain][2]:
                points[participant] += 5
            elif bet[i] == actual_finish_order[mountain][3]:
                points[participant] += 3

    sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
    total_prize_fund = sum(amounts.values())
    prize_distribution = [0.5, 0.25, 0.15, 0.1]
    prize_results = [(sorted_points[i][0], total_prize_fund * prize_distribution[i]) for i in range(min(4, len(sorted_points)))]

    return render_template('results.html', sorted_points=sorted_points, total_prize_fund=total_prize_fund, prize_results=prize_results, amounts=amounts)

if __name__ == '__main__':
    app.run(debug=True)
