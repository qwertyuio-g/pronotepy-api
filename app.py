from flask import Flask, request, jsonify
import pronotepy
import os

app = Flask(__name__)

@app.route('/grades', methods=['POST'])
def get_grades():
    data = request.json
    try:
        client = pronotepy.Client(
            'https://4010004a.index-education.net/pronote/eleve.html',
            username=data['username'],
            password=data['password']
        )
        period = client.periods[0]
        subjects = []
        for avg in period.averages:
            try:
                val = float(str(avg.student).replace(',', '.'))
                subjects.append({'name': avg.subject.name, 'average': round(val, 2)})
            except:
                pass
        try:
            general = float(str(period.overall_average).replace(',', '.'))
        except:
            general = round(sum(s['average'] for s in subjects) / len(subjects), 2) if subjects else 0
        return jsonify({'success': True, 'subjects': subjects, 'general': general})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
