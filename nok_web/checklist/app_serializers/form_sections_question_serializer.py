from rest_framework import serializers
from ..app_models.form_sections_question import Form_Sections_Question


class Form_Sections_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Sections_Question
        fields = ['id', 'question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'is_deleted']