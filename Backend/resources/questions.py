from flask.views import MethodView
from flask_smorest import Blueprint
from extensions.db import check_in_questions, custom_check_in_questions
from schemas.schemas import (
    QuestionResponseSchema,
    CustomQuestionSchema,
    CustomQuestionResponseSchema,
    DeleteCustomQuestionResponseSchema,
)

blp = Blueprint(
    "check_in_questions",
    __name__,
    description="Operations on check in shortcut questions.",
)


# Get all general check-in questions.
@blp.route("/check-in-questions")
class Questions(MethodView):

    @blp.response(200, QuestionResponseSchema(many=True))
    def get(self):
        """
        Retrieve general questions from db.
        """
        questions = list(check_in_questions.values())
        if not questions:
            return []
        return questions


# Get, post, and delete custom(created by the user) check-in questions.
@blp.route("/custom-check-in_questions/<string:user_id>")
class CustomQuestions(MethodView):

    @blp.response(200, CustomQuestionResponseSchema(many=True))
    def get(self, user_id):
        """
        Retrieve custom questions created by a specific user.
        """
        # Check if the user has any questions in the database
        user_questions = custom_check_in_questions.get(user_id, [])

        # Return an empty list and a message if no questions exist for the user
        if not user_questions:
            return []  # Return an empty list if no questions

        # Return the list of questions for the specified user
        return user_questions  # Flask-Smorest will handle the serialization

    @blp.arguments(CustomQuestionSchema, location="json")
    @blp.response(201, CustomQuestionResponseSchema)
    def post(self, question_data, user_id):
        """
        Create a new custom question for a user.
        """
        # Initialize the user's questions list if it doesn't exist
        if user_id not in custom_check_in_questions:
            custom_check_in_questions[user_id] = []

        # Generate a unique ID for the new question
        new_question = {
            "id": str(len(custom_check_in_questions[user_id]) + 1),
            "user_id": user_id,
            **question_data,
        }

        # Add the new question to the user's list of questions
        custom_check_in_questions[user_id].append(new_question)

        return new_question

    @blp.response(200, DeleteCustomQuestionResponseSchema)
    def delete(self, user_id):
        """
        Delete all custom questions for a user.
        """
        user_questions = custom_check_in_questions.get(user_id)

        if user_questions:
            custom_check_in_questions[user_id] = []
            return {
                "questions": [],
                "message": f"All questions have been deleted for user ID {user_id}",
            }

        return {"questions": [], "message": "No questions found for the user"}, 404
