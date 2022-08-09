from django.db import models
from django.urls import reverse

class Regions(models.Model):
    region_name = models.CharField(max_length=50, verbose_name='Регион')  #  verbose_name - Как поле будет отображаться в админке
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Departments(models.Model):
    department_name = models.CharField(max_length=200, verbose_name='Департамент')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    website = models.CharField(max_length=30, verbose_name='Сайт')
    email = models.EmailField(max_length=50, verbose_name='Email')
    parent = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parent_id')           # Поле для отношения к самому себе
    region = models.ForeignKey('Regions', on_delete=models.PROTECT, null=True, verbose_name='Регион_id')              #Поле для связывания моделей (в данном случае для модели Region)
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('library', kwargs={"pk": self.pk})

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class Department_Persons(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    second_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(max_length=50, blank=True, verbose_name='Email')
    department = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департамент_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    # def __str__(self):
    #     return self.department_name

    class Meta:
        verbose_name = 'Ответственный из Департамента'
        verbose_name_plural = 'Ответственные из Департаментов'


class Organisations(models.Model):
    organisation_name = models.CharField(max_length=200, verbose_name='Учреждение')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    website = models.CharField(max_length=30, verbose_name='Сайт')
    email = models.EmailField(max_length=50, verbose_name='Email')
    parent = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parent_id')
    department = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департамент_id')
    quota = models.ForeignKey('Quota', on_delete=models.PROTECT, null=True, verbose_name='Квота_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.organisation_name

    class Meta:
        verbose_name = 'Учреждение'
        verbose_name_plural = 'Учреждения'


class Organisation_Persons(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    second_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(max_length=50, blank=True, verbose_name='Email')
    organisation = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Учреждение_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Ответственный из Учреждения'
        verbose_name_plural = 'Ответственные из Учреждений'


class Quota(models.Model):
    quota = models.IntegerField(verbose_name='Квота респондентов')

    def __int__(self):
        return self.quota

    class Meta:
        verbose_name = 'Квота'
        verbose_name_plural = 'Квоты'


class Templates(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование шаблона html')
    template_file = models.FileField(verbose_name='Ссылка на шаблон')
    version = models.ForeignKey('Versions', on_delete=models.PROTECT, null=True, verbose_name='Версия_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наименование шаблона html'
        verbose_name_plural = 'Наименование шаблона html'


class Forms(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование формы Акта/Отчета')
    created_at = models.DateField(verbose_name='Дата формы')
    departments = models.ForeignKey('Departments', on_delete=models.PROTECT, null=True, verbose_name='Департаменты_id')
    templates = models.ForeignKey('Templates', on_delete=models.PROTECT, null=True, verbose_name='Шаблоны_id')
    version = models.ForeignKey('Versions', on_delete=models.PROTECT, null=True, verbose_name='Версия_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наименование формы Акта/Отчета'


class Form_Sections(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование разделов')
    version = models.CharField(max_length=20, verbose_name='Версия раздела')
    order_num = models.IntegerField(verbose_name='Порядковый номер')
    parent = models.ForeignKey('Form_Sections', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Parent_id')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наименование разделов'


class Questions(models.Model):
    name = models.CharField(max_length=250, verbose_name='Вопросы')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Варианты вопросов'


class Question_Values(models.Model):
    value_name = models.CharField(max_length=50, verbose_name='Варианты ответов')
    questions = models.ForeignKey('Questions', on_delete=models.PROTECT, null=True, verbose_name='Вопросы_id')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.value_name

    class Meta:
        verbose_name_plural = 'Варианты ответов'


class Form_Sections_Question(models.Model):
    questions = models.ForeignKey('Questions', on_delete=models.PROTECT, null=True, verbose_name='Вопросы_id')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    order_num = models.IntegerField(verbose_name='Порядковый номер')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Сопоставление вопрос-форма'


class Recommendations(models.Model):
    name = models.CharField(max_length=250, verbose_name='Рекоммендации')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Варианты рекоммендаций'


class Forms_Recommendations(models.Model):
    free_value = models.CharField(max_length=250, verbose_name='Рекомендации в свободной форме')
    answers = models.ForeignKey('Answers', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Ответы_id')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    form_sections = models.ForeignKey('Form_Sections', on_delete=models.PROTECT, null=True, verbose_name='Разделы_id')
    recommendations = models.ForeignKey('Recommendations', on_delete=models.PROTECT, null=True, verbose_name='Рекоммендации_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Рекомендации - факт'


class Answers(models.Model):
    free_value = models.CharField(max_length=250, verbose_name='Ответы в свободной форме')
    organisations = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Организации_id')
    quota = models.ForeignKey('Quota', on_delete=models.PROTECT, null=True, verbose_name='Квоты_id')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    questions = models.ForeignKey('Questions', on_delete=models.PROTECT, null=True, verbose_name='Вопросы_id')
    question_values = models.ForeignKey('Question_Values', on_delete=models.PROTECT, null=True, verbose_name='Варианты ответов_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Ответы - факт'


class Signed_Dociuments(models.Model):
    file_name = models.CharField(max_length=100, verbose_name='Наименования документов')
    originat_file_name = models.FileField(verbose_name='Ссылка на документ')
    description = models.CharField(max_length=250, verbose_name='Комментарий')
    created_at = models.DateField(verbose_name='Дата документа')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    evaluation = models.ForeignKey('Evaluation', on_delete=models.PROTECT, null=True, verbose_name='Оценка_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Подписанные Акты'

    def __str__(self):
        return self.file_name


class Evaluation(models.Model):
    date_evaluation = models.DateField(verbose_name='Дата проведения оценки')
    forms = models.ForeignKey('Forms', on_delete=models.PROTECT, null=True, verbose_name='Формы_id')
    organisations = models.ForeignKey('Organisations', on_delete=models.PROTECT, null=True, verbose_name='Организации_id')
    organisation_persons = models.ForeignKey('Organisation_Persons', on_delete=models.PROTECT, null=True, verbose_name='Представитель организации_id')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Независимая оценка'


class Versions(models.Model):
    table_name = models.CharField(max_length=50, verbose_name='Таблица')
    version = models.CharField(max_length=50, verbose_name='Версия')
    active = models.BooleanField(default=True, verbose_name='Текущая версия')
    is_deleted = models.BooleanField(default=False, verbose_name='Признак удаления')

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.table_name

    class Meta:
        verbose_name_plural = 'Контроль версий'