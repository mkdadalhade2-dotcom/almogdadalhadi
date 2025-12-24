from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# قاعدة بيانات التخصصات
SCIENCE_MAJORS = [
    {"id": 1, "name": "هندسة الحاسوب", "description": "تصميم وتطوير الأنظمة البرمجية والمعدنية"},
    {"id": 2, "name": "الطب البشري", "description": "تشخيص وعلاج الأمراض والوقاية منها"},
    {"id": 3, "name": "هندسة الكهرباء", "description": "تصميم الأنظمة الكهربائية والإلكترونية"},
    {"id": 4, "name": "الصيدلة", "description": "دراسة الأدوية وتحضيرها وتوزيعها"},
    {"id": 5, "name": "علوم الحاسوب", "description": "دراسة الخوارزميات والبرمجة والذكاء الاصطناعي"}
]

LITERARY_MAJORS = [
    {"id": 6, "name": "إدارة الأعمال", "description": "تخطيط وتنظيم وإدارة المؤسسات"},
    {"id": 7, "name": "اللغة العربية", "description": "دراسة الأدب العربي والنحو والصرف"},
    {"id": 8, "name": "الإعلام", "description": "الإذاعة والتلفزيون والصحافة الرقمية"},
    {"id": 9, "name": "القانون", "description": "دراسة التشريعات والنظم القانونية"},
    {"id": 10, "name": "اللغة الإنجليزية", "description": "دراسة الأدب الإنجليزي والترجمة"}
]

def analyze_science_grades(math, physics, chemistry, biology):
    results = []
    
    # هندسة الحاسوب
    eng_score = math * 0.4 + physics * 0.3 + chemistry * 0.2 + biology * 0.1
    results.append({
        **SCIENCE_MAJORS[0],
        "match": min(100, int(eng_score)),
        "reasons": ["تفوق في الرياضيات", "قدرة تحليلية عالية"] if math > 80 else ["درجات متوازنة"]
    })
    
    # الطب البشري
    med_score = math * 0.2 + physics * 0.2 + chemistry * 0.3 + biology * 0.3
    results.append({
        **SCIENCE_MAJORS[1],
        "match": min(100, int(med_score)),
        "reasons": ["تفوق في الأحياء", "ميل للعلوم الطبية"] if biology > 85 else ["درجات علمية جيدة"]
    })
    
    # هندسة الكهرباء
    elec_score = math * 0.5 + physics * 0.4 + chemistry * 0.05 + biology * 0.05
    results.append({
        **SCIENCE_MAJORS[2],
        "match": min(100, int(elec_score)),
        "reasons": ["تميز في الرياضيات والفيزياء", "قدرة على التطبيق العملي"] if math > 75 and physics > 75 else ["قدرات هندسية"]
    })
    
    # ترتيب النتائج
    results.sort(key=lambda x: x["match"], reverse=True)
    return results[:3]

def analyze_literary_grades(arabic, english, history, geography):
    results = []
    
    # إدارة الأعمال
    bus_score = arabic * 0.3 + english * 0.4 + history * 0.15 + geography * 0.15
    results.append({
        **LITERARY_MAJORS[0],
        "match": min(100, int(bus_score)),
        "reasons": ["مستوى جيد في الإنجليزية", "قدرة على التواصل"] if english > 75 else ["قدرات إدارية"]
    })
    
    # اللغة العربية
    arabic_score = arabic * 0.6 + english * 0.2 + history * 0.1 + geography * 0.1
    results.append({
        **LITERARY_MAJORS[1],
        "match": min(100, int(arabic_score)),
        "reasons": ["تفوق في اللغة العربية", "قدرة تعبيرية"] if arabic > 85 else ["قدرات لغوية"]
    })
    
    # الإعلام
    media_score = arabic * 0.4 + english * 0.3 + history * 0.15 + geography * 0.15
    results.append({
        **LITERARY_MAJORS[2],
        "match": min(100, int(media_score)),
        "reasons": ["قدرة على التعبير", "مهارات اتصالية"] if arabic > 70 else ["قدرات إعلامية"]
    })
    
    # ترتيب النتائج
    results.sort(key=lambda x: x["match"], reverse=True)
    return results[:3]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    try:
        stream = data['stream']
        grades = data['grades']
        
        if stream == 'science':
            math = grades.get('math', 0)
            physics = grades.get('physics', 0)
            chemistry = grades.get('chemistry', 0)
            biology = grades.get('biology', 0)
            
            results = analyze_science_grades(math, physics, chemistry, biology)
        else:
            arabic = grades.get('arabic', 0)
            english = grades.get('english', 0)
            history = grades.get('history', 0)
            geography = grades.get('geography', 0)
            
            results = analyze_literary_grades(arabic, english, history, geography)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'تم التحليل بنجاح'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ: {str(e)}'
        })

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "النظام الذكي للتوجيه الأكاديمي",
        "short_name": "SmartAdvisor",
        "start_url": "/",
        "display": "standalone",
        "theme_color": "#2c3e50",
        "background_color": "#ffffff"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)