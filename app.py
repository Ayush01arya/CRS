from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Career pathways with required attributes
career_pathways = {
    "Software Engineering": {
        "description": "Develop, test, and maintain software applications and systems.",
        "education": ["Computer Science", "Software Engineering", "Information Technology"],
        "skills": ["Programming", "Problem-solving", "Logical thinking"],
        "matches": {
            "academic": ["cs_programming_ability >= 4", "math_ability >= 3"],
            "interest": ["cs_programming_interest >= 4", "investigative_score >= 20"],
            "aptitude": ["logical_reasoning_score >= 15", "numerical_reasoning_score >= 14"],
            "personality": ["openness_score >= 12", "conscientiousness_score >= 14"],
            "values": ["growth_learning_value >= 4", "challenge_value >= 3"]
        }
    },
    "Data Science": {
        "description": "Analyze and interpret complex data to inform business decisions.",
        "education": ["Statistics", "Mathematics", "Computer Science", "Data Science"],
        "skills": ["Statistical analysis", "Programming", "Machine learning"],
        "matches": {
            "academic": ["math_ability >= 4", "cs_programming_ability >= 3"],
            "interest": ["investigative_score >= 22", "math_interest >= 4"],
            "aptitude": ["numerical_reasoning_score >= 16", "logical_reasoning_score >= 15"],
            "personality": ["openness_score >= 14", "conscientiousness_score >= 15"],
            "values": ["problem_solving_value >= 4", "analytical_thinking_value >= 4"]
        }
    },
    "Healthcare": {
        "description": "Diagnose, treat, and help prevent diseases and injuries.",
        "education": ["Medicine", "Nursing", "Public Health", "Biology"],
        "skills": ["Patient care", "Medical knowledge", "Communication"],
        "matches": {
            "academic": ["biology_ability >= 4", "chemistry_ability >= 3"],
            "interest": ["social_score >= 20", "biology_interest >= 4"],
            "aptitude": ["verbal_reasoning_score >= 15", "numerical_reasoning_score >= 14"],
            "personality": ["agreeableness_score >= 16", "conscientiousness_score >= 16"],
            "values": ["helping_others_value >= 4", "social_impact_value >= 4"]
        }
    },
    "Business Management": {
        "description": "Plan, direct, and coordinate the operations of an organization.",
        "education": ["Business Administration", "Management", "Economics"],
        "skills": ["Leadership", "Communication", "Decision-making"],
        "matches": {
            "academic": ["history_social_ability >= 3", "writing_composition_ability >= 3"],
            "interest": ["enterprising_score >= 20", "social_score >= 18"],
            "aptitude": ["verbal_reasoning_score >= 14", "logical_reasoning_score >= 14"],
            "personality": ["extraversion_score >= 16", "conscientiousness_score >= 15"],
            "values": ["leadership_preference >= 4", "recognition_value >= 3"]
        }
    },
    "Creative Arts": {
        "description": "Create and perform works of art, music, design, or writing.",
        "education": ["Fine Arts", "Design", "Music", "Creative Writing"],
        "skills": ["Creativity", "Aesthetic sense", "Technical skills"],
        "matches": {
            "academic": ["art_design_ability >= 4", "music_ability >= 3", "writing_composition_ability >= 3"],
            "interest": ["artistic_score >= 24", "creative_work_preference >= 4"],
            "aptitude": ["creative_thinking_score >= 16", "spatial_reasoning_score >= 14"],
            "personality": ["openness_score >= 18", "emotional_stability_score >= 12"],
            "values": ["creativity_value >= 5", "self_expression_value >= 4"]
        }
    },
    "Education": {
        "description": "Instruct and guide students in academic, social, and personal development.",
        "education": ["Education", "Teaching", "Subject specialization"],
        "skills": ["Communication", "Patience", "Organization"],
        "matches": {
            "academic": ["writing_composition_ability >= 3", "any subject with ability >= 4"],
            "interest": ["social_score >= 22", "teaching_interest >= 4"],
            "aptitude": ["verbal_reasoning_score >= 16", "creative_thinking_score >= 14"],
            "personality": ["agreeableness_score >= 16", "extraversion_score >= 14"],
            "values": ["helping_others_value >= 4", "mentorship_value >= 4"]
        }
    },
    "Engineering": {
        "description": "Apply scientific and mathematical principles to develop solutions.",
        "education": ["Engineering", "Physics", "Applied Mathematics"],
        "skills": ["Problem-solving", "Technical knowledge", "Analytical thinking"],
        "matches": {
            "academic": ["math_ability >= 4", "physics_ability >= 4"],
            "interest": ["realistic_score >= 20", "investigative_score >= 18"],
            "aptitude": ["spatial_reasoning_score >= 16", "numerical_reasoning_score >= 16"],
            "personality": ["conscientiousness_score >= 16", "openness_score >= 14"],
            "values": ["challenge_value >= 4", "problem_solving_value >= 4"]
        }
    },
    "Finance": {
        "description": "Manage money, investments, and financial systems.",
        "education": ["Finance", "Accounting", "Economics", "Business"],
        "skills": ["Numerical analysis", "Attention to detail", "Decision-making"],
        "matches": {
            "academic": ["math_ability >= 4", "cs_programming_ability >= 3"],
            "interest": ["conventional_score >= 20", "enterprising_score >= 18"],
            "aptitude": ["numerical_reasoning_score >= 16", "logical_reasoning_score >= 15"],
            "personality": ["conscientiousness_score >= 16", "emotional_stability_score >= 14"],
            "values": ["income_potential_value >= 4", "job_security_value >= 4"]
        }
    },
    "Science Research": {
        "description": "Conduct research to expand knowledge in various scientific fields.",
        "education": ["Physics", "Chemistry", "Biology", "Earth Science"],
        "skills": ["Research methodology", "Critical thinking", "Scientific writing"],
        "matches": {
            "academic": ["any science ability >= 4", "math_ability >= 3"],
            "interest": ["investigative_score >= 24", "any science interest >= 4"],
            "aptitude": ["logical_reasoning_score >= 16", "numerical_reasoning_score >= 15"],
            "personality": ["openness_score >= 16", "conscientiousness_score >= 15"],
            "values": ["expertise_value >= 4", "discovery_learning_preference >= 4"]
        }
    },
    "Social Work": {
        "description": "Help people solve and cope with problems in their everyday lives.",
        "education": ["Social Work", "Psychology", "Sociology"],
        "skills": ["Empathy", "Communication", "Problem-solving"],
        "matches": {
            "academic": ["history_social_ability >= 3", "writing_composition_ability >= 3"],
            "interest": ["social_score >= 24", "helping_others_value >= 4"],
            "aptitude": ["verbal_reasoning_score >= 15", "creative_thinking_score >= 14"],
            "personality": ["agreeableness_score >= 18", "emotional_stability_score >= 14"],
            "values": ["social_impact_value >= 5", "helping_others_value >= 5"]
        }
    }
}


# Helper function to evaluate a rule against user data
def evaluate_rule(rule, user_data):
    try:
        # Parse the rule (e.g., "math_ability >= 4")
        parts = rule.split()
        attribute = parts[0]
        operator = parts[1]
        value = float(parts[2])

        # Get the user's value for this attribute
        user_value = user_data.get(attribute, 0)

        # Handle special case for "any subject with ability >= 4"
        if attribute == "any":
            subject_type = parts[1]
            if subject_type == "science":
                abilities = ["physics_ability", "chemistry_ability", "biology_ability"]
                return any(user_data.get(ability, 0) >= value for ability in abilities)
            elif subject_type == "subject" and "ability" in parts[2]:
                abilities = [key for key in user_data.keys() if key.endswith("_ability")]
                return any(user_data.get(ability, 0) >= value for ability in abilities)

        # Evaluate the rule
        if operator == ">=":
            return user_value >= value
        elif operator == ">":
            return user_value > value
        elif operator == "<=":
            return user_value <= value
        elif operator == "<":
            return user_value < value
        elif operator == "==":
            return user_value == value
        else:
            return False
    except (IndexError, ValueError):
        return False


# Calculate match score for a career based on user data
def calculate_match_score(career, user_data):
    score = 0
    total_rules = 0
    categories = ["academic", "interest", "aptitude", "personality", "values"]

    for category in categories:
        if category in career["matches"]:
            rules = career["matches"][category]
            total_rules += len(rules)

            for rule in rules:
                if evaluate_rule(rule, user_data):
                    score += 1

    if total_rules == 0:
        return 0

    return (score / total_rules) * 100


@app.route('/api/careers', methods=['POST'])
def get_career_recommendations():
    try:
        user_data = request.json

        # Calculate match scores for each career
        results = []
        for career_name, career_info in career_pathways.items():
            match_score = calculate_match_score(career_info, user_data)

            if match_score >= 50:  # Only include careers with at least 50% match
                results.append({
                    "career": career_name,
                    "match_score": round(match_score, 1),
                    "description": career_info["description"],
                    "education": career_info["education"],
                    "skills": career_info["skills"]
                })

        # Sort results by match score (descending)
        results.sort(key=lambda x: x["match_score"], reverse=True)

        # Return top 5 recommendations
        return jsonify({
            "recommendations": results[:5],
            "total_matches": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/questionnaire', methods=['GET'])
def get_questionnaire():
    questionnaire = [
        {
            "id": 1,
            "question": "How would you rate your math ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "math_ability"
        },
        {
            "id": 2,
            "question": "How would you rate your interest in computer programming?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "cs_programming_interest"
        },
        {
            "id": 3,
            "question": "How would you rate your ability in biology?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "biology_ability"
        },
        {
            "id": 4,
            "question": "How would you rate your interest in helping others?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "helping_others_value"
        },
        {
            "id": 5,
            "question": "How would you rate your logical reasoning ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "logical_reasoning_score"
        },
        {
            "id": 6,
            "question": "How would you rate your creativity?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "creative_thinking_score"
        },
        {
            "id": 7,
            "question": "How would you rate your writing ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "writing_composition_ability"
        },
        {
            "id": 8,
            "question": "How would you rate your leadership preference?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "leadership_preference"
        },
        {
            "id": 9,
            "question": "How would you rate your preference for teamwork?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "team_collaboration_value"
        },
        {
            "id": 10,
            "question": "How would you rate your interest in artistic activities?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "artistic_score"
        },
        {
            "id": 11,
            "question": "How would you rate your preference for structured tasks?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "structured_task_preference"
        },
        {
            "id": 12,
            "question": "How would you rate your interest in scientific research?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "investigative_score"
        },
        {
            "id": 13,
            "question": "How would you rate your interest in social impact?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "social_impact_value"
        },
        {
            "id": 14,
            "question": "How would you rate your verbal reasoning ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "verbal_reasoning_score"
        },
        {
            "id": 15,
            "question": "How would you rate your interest in business and entrepreneurship?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "enterprising_score"
        },
        {
            "id": 16,
            "question": "How would you rate the importance of income potential in your career choice?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "income_potential_value"
        },
        {
            "id": 17,
            "question": "How would you rate your interest in teaching others?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "teaching_interest"
        },
        {
            "id": 18,
            "question": "How would you rate your ability to work under pressure?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "emotional_stability_score"
        },
        {
            "id": 19,
            "question": "How would you rate your interest in creative work?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "creative_work_preference"
        },
        {
            "id": 20,
            "question": "How would you rate the importance of work-life balance in your career choice?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "work_life_balance_value"
        }
    ]

    return jsonify(questionnaire)


if __name__ == '__main__':
    app.run(debug=True, port=5000)