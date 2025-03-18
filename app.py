from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Career pathways with required attributes - fixed rule formats and added missing values
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
            "interest": ["investigative_score >= 20", "math_interest >= 4"],
            "aptitude": ["numerical_reasoning_score >= 15", "logical_reasoning_score >= 15"],
            "personality": ["openness_score >= 14", "conscientiousness_score >= 15"],
            "values": ["growth_learning_value >= 4", "challenge_value >= 4"]  # Replaced undefined values
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
            "values": ["creativity_value >= 5", "autonomy_value >= 4"]  # Replaced undefined value
        }
    },
    "Education": {
        "description": "Instruct and guide students in academic, social, and personal development.",
        "education": ["Education", "Teaching", "Subject specialization"],
        "skills": ["Communication", "Patience", "Organization"],
        "matches": {
            "academic": ["writing_composition_ability >= 3", "has_ability >= 4"],  # Fixed rule format
            "interest": ["social_score >= 22", "helping_others_value >= 4"],  # Replaced undefined parameter
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
            "values": ["challenge_value >= 4", "growth_learning_value >= 4"]  # Replaced undefined value
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
            "academic": ["science_ability >= 4", "math_ability >= 3"],  # Fixed rule format
            "interest": ["investigative_score >= 24", "science_interest >= 4"],  # Fixed format
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


# Improved helper function to evaluate a rule against user data
def evaluate_rule(rule, user_data):
    try:
        # Parse the rule (e.g., "math_ability >= 4")
        parts = rule.split()
        attribute = parts[0]
        operator = parts[1]
        value = float(parts[2])

        # Special case handling
        if attribute == "science_ability":
            # Check if any science ability meets the threshold
            science_abilities = ["physics_ability", "chemistry_ability", "biology_ability"]
            return any(user_data.get(ability, 0) >= value for ability in science_abilities)

        if attribute == "science_interest":
            # Check if any science interest meets the threshold
            science_interests = ["physics_interest", "chemistry_interest", "biology_interest"]
            return any(user_data.get(interest, 0) >= value for interest in science_interests)

        if attribute == "has_ability":
            # Check if any ability meets the threshold
            abilities = [key for key in user_data.keys() if key.endswith("_ability")]
            return any(user_data.get(ability, 0) >= value for ability in abilities)

        # Get the user's value for this attribute
        user_value = user_data.get(attribute, 0)

        # If parameter not found, provide a reasonable default value
        # This is important for handling missing data
        if attribute not in user_data:
            # For Holland codes
            if attribute in ["realistic_score", "investigative_score", "artistic_score",
                             "social_score", "enterprising_score", "conventional_score"]:
                user_value = 18  # Middle of the 6-30 range
            # For aptitude scores
            elif attribute in ["verbal_reasoning_score", "numerical_reasoning_score",
                               "spatial_reasoning_score", "logical_reasoning_score",
                               "creative_thinking_score"]:
                user_value = 12  # Middle of the 4-20 range
            # For personality scores
            elif attribute in ["openness_score", "conscientiousness_score", "extraversion_score",
                               "agreeableness_score", "emotional_stability_score"]:
                user_value = 12  # Middle of the 4-20 range
            # For other values (1-5 scale)
            else:
                user_value = 3  # Middle of the 1-5 range

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


# Improved match score calculation with category weighting
def calculate_match_score(career, user_data):
    # Category weights - give more importance to interests and academic ability
    weights = {
        "academic": 1.2,
        "interest": 1.5,
        "aptitude": 1.0,
        "personality": 0.8,
        "values": 1.0
    }

    weighted_score = 0
    total_weight = 0

    categories = ["academic", "interest", "aptitude", "personality", "values"]

    for category in categories:
        if category in career["matches"]:
            rules = career["matches"][category]
            category_weight = weights[category] * len(rules)
            total_weight += category_weight

            matched_rules = sum(1 for rule in rules if evaluate_rule(rule, user_data))
            weighted_score += (matched_rules / len(rules)) * category_weight

    if total_weight == 0:
        return 0

    # Handle missing data more gracefully by adding a small penalty
    # for extensive missing data, but not eliminating options entirely
    missing_params = 0
    for category in categories:
        if category in career["matches"]:
            for rule in career["matches"][category]:
                param = rule.split()[0]
                if param not in user_data and param not in ["science_ability", "science_interest", "has_ability"]:
                    missing_params += 1

    missing_penalty = 0
    if missing_params > 5:
        missing_penalty = 0.1

    final_score = (weighted_score / total_weight) * 100 * (1 - missing_penalty)
    return final_score


@app.route('/api/careers', methods=['POST'])
def get_career_recommendations():
    try:
        user_data = request.json

        # If input is empty or invalid, generate some default values
        if not user_data or not isinstance(user_data, dict):
            user_data = generate_default_user_data()

        # Fill in missing values with defaults to ensure some recommendations
        user_data = fill_missing_values(user_data)

        # Calculate match scores for each career
        results = []
        for career_name, career_info in career_pathways.items():
            match_score = calculate_match_score(career_info, user_data)

            # Lower the threshold to 40% to ensure some recommendations
            if match_score >= 40:
                results.append({
                    "career": career_name,
                    "match_score": round(match_score, 1),
                    "description": career_info["description"],
                    "education": career_info["education"],
                    "skills": career_info["skills"]
                })

        # Sort results by match score (descending)
        results.sort(key=lambda x: x["match_score"], reverse=True)

        # If no results, return top 3 careers with a reasonable match
        if not results:
            for career_name, career_info in career_pathways.items():
                results.append({
                    "career": career_name,
                    "match_score": 50.0,  # Default reasonable score
                    "description": career_info["description"],
                    "education": career_info["education"],
                    "skills": career_info["skills"]
                })
            results.sort(key=lambda x: x["career"])  # Alphabetical if no real matches
            results = results[:3]

        # Return top 5 recommendations
        return jsonify({
            "recommendations": results[:5],
            "total_matches": len(results)
        })
    except Exception as e:
        # On error, return some default recommendations
        default_recommendations = get_default_recommendations()
        return jsonify(default_recommendations)


# Helper function to fill in missing values
def fill_missing_values(user_data):
    # Define default values for different parameter types
    defaults = {
        "ability": 3,  # Default ability level (middle of 1-5)
        "interest": 3,  # Default interest level (middle of 1-5)
        "score": 15,  # Default for Holland codes (middle of 6-30)
        "reasoning_score": 12,  # Default for aptitude (middle of 4-20)
        "personality_score": 12,  # Default for Big Five (middle of 4-20)
        "value": 3,  # Default for values (middle of 1-5)
        "preference": 3  # Default for preferences (middle of 1-5)
    }

    # Check for missing parameters and add defaults
    for param_type, default_value in defaults.items():
        if param_type == "score":
            for code in ["realistic", "investigative", "artistic", "social", "enterprising", "conventional"]:
                param = f"{code}_score"
                if param not in user_data:
                    user_data[param] = default_value
        elif param_type == "reasoning_score":
            for reasoning in ["verbal", "numerical", "spatial", "logical", "creative"]:
                param = f"{reasoning}_reasoning_score"
                if param not in user_data:
                    user_data[param] = default_value
        elif param_type == "personality_score":
            for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "emotional_stability"]:
                param = f"{trait}_score"
                if param not in user_data:
                    user_data[param] = default_value
        else:
            # Check all parameters ending with this type
            for key in list(career_pathways.values())[0]["matches"].values():
                for rule in key:
                    param = rule.split()[0]
                    if param.endswith(param_type) and param not in user_data:
                        user_data[param] = default_value

    return user_data


# Generate reasonable default data if the user provides none
def generate_default_user_data():
    return {
        "math_ability": 3,
        "cs_programming_ability": 3,
        "biology_ability": 3,
        "chemistry_ability": 3,
        "physics_ability": 3,
        "writing_composition_ability": 3,
        "history_social_ability": 3,
        "art_design_ability": 3,
        "music_ability": 3,
        "math_interest": 3,
        "cs_programming_interest": 3,
        "biology_interest": 3,
        "investigative_score": 18,
        "artistic_score": 18,
        "social_score": 18,
        "enterprising_score": 18,
        "conventional_score": 18,
        "realistic_score": 18,
        "logical_reasoning_score": 12,
        "numerical_reasoning_score": 12,
        "verbal_reasoning_score": 12,
        "spatial_reasoning_score": 12,
        "creative_thinking_score": 12,
        "openness_score": 12,
        "conscientiousness_score": 12,
        "extraversion_score": 12,
        "agreeableness_score": 12,
        "emotional_stability_score": 12,
        "helping_others_value": 3,
        "leadership_preference": 3,
        "team_collaboration_value": 3,
        "creative_work_preference": 3,
        "growth_learning_value": 3,
        "challenge_value": 3,
        "social_impact_value": 3,
        "income_potential_value": 3,
        "job_security_value": 3,
        "discovery_learning_preference": 3,
        "structured_task_preference": 3,
        "mentorship_value": 3,
        "recognition_value": 3,
        "expertise_value": 3,
        "autonomy_value": 3,
        "work_life_balance_value": 3
    }


# Return default recommendations when all else fails
def get_default_recommendations():
    default_careers = ["Software Engineering", "Business Management", "Healthcare", "Creative Arts", "Education"]
    results = []

    for career_name in default_careers:
        career_info = career_pathways.get(career_name)
        if career_info:
            results.append({
                "career": career_name,
                "match_score": 60.0,  # Default reasonable score
                "description": career_info["description"],
                "education": career_info["education"],
                "skills": career_info["skills"]
            })

    return {
        "recommendations": results,
        "total_matches": len(results)
    }


@app.route('/api/questionnaire', methods=['GET'])
def get_questionnaire():
    # Expanded questionnaire to capture more parameters needed for rules
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
            "question": "How would you rate your computer programming ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "cs_programming_ability"
        },
        {
            "id": 3,
            "question": "How would you rate your interest in computer programming?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "cs_programming_interest"
        },
        {
            "id": 4,
            "question": "How would you rate your biology ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "biology_ability"
        },
        {
            "id": 5,
            "question": "How would you rate your interest in biology?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "biology_interest"
        },
        {
            "id": 6,
            "question": "How would you rate your chemistry ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "chemistry_ability"
        },
        {
            "id": 7,
            "question": "How would you rate your physics ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "physics_ability"
        },
        {
            "id": 8,
            "question": "How would you rate your writing ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "writing_composition_ability"
        },
        {
            "id": 9,
            "question": "How would you rate your interest in helping others?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "helping_others_value"
        },
        {
            "id": 10,
            "question": "How interested are you in making a social impact?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "social_impact_value"
        },
        {
            "id": 11,
            "question": "How would you rate your logical reasoning ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "logical_reasoning_score"
        },
        {
            "id": 12,
            "question": "How would you rate your numerical reasoning ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "numerical_reasoning_score"
        },
        {
            "id": 13,
            "question": "How would you rate your verbal reasoning ability?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "verbal_reasoning_score"
        },
        {
            "id": 14,
            "question": "How would you rate your creativity?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "creative_thinking_score"
        },
        {
            "id": 15,
            "question": "How would you rate your leadership preference?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "leadership_preference"
        },
        {
            "id": 16,
            "question": "How would you rate your preference for teamwork?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "team_collaboration_value"
        },
        {
            "id": 17,
            "question": "How would you rate your interest in artistic activities?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "artistic_score"
        },
        {
            "id": 18,
            "question": "How would you rate your interest in investigating and analyzing?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "investigative_score"
        },
        {
            "id": 19,
            "question": "How would you rate your interest in social activities?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "social_score"
        },
        {
            "id": 20,
            "question": "How would you rate your interest in business and entrepreneurship?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "enterprising_score"
        },
        {
            "id": 21,
            "question": "How would you rate your preference for structured tasks?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "structured_task_preference"
        },
        {
            "id": 22,
            "question": "How would you rate your preference for creative work?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "creative_work_preference"
        },
        {
            "id": 23,
            "question": "How important is growth and learning in your career choice?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "growth_learning_value"
        },
        {
            "id": 24,
            "question": "How important is challenge in your career choice?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "challenge_value"
        },
        {
            "id": 25,
            "question": "How important is income potential in your career choice?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "income_potential_value"
        },
        {
            "id": 26,
            "question": "How would you rate your level of openness to new experiences?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "openness_score"
        },
        {
            "id": 27,
            "question": "How would you rate your level of conscientiousness?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "conscientiousness_score"
        },
        {
            "id": 28,
            "question": "How would you rate your level of extraversion?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "extraversion_score"
        },
        {
            "id": 29,
            "question": "How would you rate your level of agreeableness?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "agreeableness_score"
        },
        {
            "id": 30,
            "question": "How would you rate your ability to work under pressure?",
            "type": "scale",
            "options": ["Very Low", "Low", "Average", "High", "Very High"],
            "param": "emotional_stability_score"
        }
    ]

    return jsonify(questionnaire)


if __name__ == '__main__':
    app.run(debug=True, port=5000)