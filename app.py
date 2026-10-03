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
                class_val = None
                try:
                    class_val = float(str(avg.class_average).replace(',', '.'))
                except:
                    pass
                subjects.append({
                    'name': avg.subject.name,
                    'average': val,
                    'class_average': class_val
                })
            except:
                pass

        try:
            general = float(str(period.overall_average).replace(',', '.'))
        except:
            general = round(sum(s['average'] for s in subjects) / len(subjects), 2) if subjects else 0

        # Moyenne générale de classe
        try:
            general_class = float(str(period.class_overall_average).replace(',', '.'))
        except:
            class_avgs = [s['class_average'] for s in subjects if s['class_average'] is not None]
            general_class = round(sum(class_avgs) / len(class_avgs), 2) if class_avgs else None

        return jsonify({
            'success': True,
            'subjects': subjects,
            'general': general,
            'general_class_average': general_class
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
