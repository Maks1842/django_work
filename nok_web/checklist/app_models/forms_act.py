from django.db import models

'''
Хранятся json структуры Актов, используемых в проверке.
На основе act_json формируются поля анкеты на фронтенде.
Также структура act_json используется при сопоставлении с answers_json (json структура ответов), при рендеринге 
HTML шаблона, Акта проверки с результатами.
'''


class FormsAct(models.Model):
    type_departments = models.ForeignKey('Type_Departments', on_delete=models.PROTECT, null=True,
                                         verbose_name='Тип департамента')
    type_organisations = models.ForeignKey('Type_Organisations', on_delete=models.PROTECT, null=True, blank=True,
                                           verbose_name='Тип учреждения')
    act_json = models.JSONField(verbose_name='Структура акта')
    date = models.DateField(null=True, blank=True, verbose_name='Дата формы акта')
    version = models.CharField(max_length=50, verbose_name='Версия формы акта')

    class Meta:
        verbose_name_plural = 'Формы актов'
