import zoneinfo
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    UserProfile, AboutCompany, NewsArticle, FAQItem, ContactEmployee,
    JobVacancy, PrivacyPolicy, Country, Genre, Movie, CinemaHall,
    Showtime, StaffProfile, Ticket, PromoCode, Review
)


# 1. Форма для отображения полей встроенного User
class UserProfileAdminForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя (Логин)", max_length=150)
    email = forms.EmailField(label="Электронная почта", required=False)
    first_name = forms.CharField(label="Имя", max_length=150, required=False)
    last_name = forms.CharField(label="Фамилия", max_length=150, required=False)
    is_active = forms.BooleanField(label="Активен", required=False)
    is_staff = forms.BooleanField(label="Статус персонала (Сотрудник)", required=False)
    is_superuser = forms.BooleanField(label="Статус суперпользователя (Админ)", required=False)

    class Meta:
        model = UserProfile
        fields = ['photo', 'age', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs.update({
                'placeholder': '+375 (XX) XXX-XX-XX',
                'oninput': "let matrix = '+375 (__) ___-__-__', i = 0, def = matrix.replace(/\\D/g, ''), val = this.value.replace(/\\D/g, ''); if (def.length >= val.length) val = def; this.value = matrix.replace(/./g, function(a) { return /[_\\d]/.test(a) && i < val.length ? val.charAt(i++) : i >= val.length ? '' : a; });"
            })
        # Подгружаем данные из связанного User при открытии аннотации
        if self.instance and self.instance.pk and hasattr(self.instance, 'user'):
            user = self.instance.user
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['is_active'].initial = user.is_active
            self.fields['is_staff'].initial = user.is_staff
            self.fields['is_superuser'].initial = user.is_superuser


# 2. Сама админка Пользователей
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm

    list_display = ('get_username', 'get_email', 'phone', 'age')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('age',)

    fieldsets = (
        ('Данные учетной записи (Django User)', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Личные данные профиля', {
            'fields': ('photo', 'age', 'phone')
        }),
        ('Права доступа и статусы', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Системные даты (Только чтение)', {
            'fields': ('get_date_joined', 'get_last_login', 'created_at_local', 'updated_at_local'),
        }),
    )

    readonly_fields = ('get_date_joined', 'get_last_login', 'created_at_local', 'updated_at_local')

    # Переопределяем сохранение модели в админке
    def save_model(self, request, obj, form, change):
        user = obj.user

        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.is_active = form.cleaned_data['is_active']
        user.is_staff = form.cleaned_data['is_staff']
        user.is_superuser = form.cleaned_data['is_superuser']

        user.save()
        super().save_model(request, obj, form, change)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Логин'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    def get_date_joined(self, obj):
        if obj.user.date_joined:
            minsk_tz = zoneinfo.ZoneInfo("Europe/Minsk")
            return obj.user.date_joined.astimezone(minsk_tz).strftime("%d/%m/%Y %H:%M:%S")
        return "-"

    get_date_joined.short_description = "Дата регистрации"

    def get_last_login(self, obj):
        if obj.user.last_login:
            minsk_tz = zoneinfo.ZoneInfo("Europe/Minsk")
            return obj.user.last_login.astimezone(minsk_tz).strftime("%d/%m/%Y %H:%M:%S")
        return "-"

    get_last_login.short_description = "Последний вход"

    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/imask/6.4.3/imask.min.js',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'phone':
            field.widget.attrs['class'] = 'phone-mask'
        return field


@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'logo')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at_local')
    search_fields = ('title', 'short_description')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at_local')


@admin.register(ContactEmployee)
class ContactEmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone', 'email')
    search_fields = ('full_name', 'position')


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active')
    list_filter = ('is_active',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1
    readonly_fields = ('created_at_local', 'updated_at_local')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'duration', 'display_countries', 'rating', 'budget')
    list_filter = ('genres', 'countries')
    search_fields = ('title_ru', 'title_en', 'description')

    def display_title(self, obj):
        return f"{obj.title_ru} ({obj.title_en})"

    display_title.short_description = 'Название фильма'

    def display_countries(self, obj):
        countries_list = [c.name for c in obj.countries.all()]
        return ", ".join(countries_list) if countries_list else "Не указаны"

    display_countries.short_description = 'Страны производства'


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'ticket_price')
    list_filter = ('hall', 'start_time')
    date_hierarchy = 'start_time'
    inlines = [TicketInline]


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'birth_date')
    search_fields = ('user__username', 'position')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'showtime', 'customer', 'row', 'seat', 'created_at_local')
    search_fields = ('customer__username', 'showtime__movie__title_ru')
    list_filter = ('created_at_local',)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'is_active', 'created_at_local')
    list_filter = ('is_active',)
    search_fields = ('code', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at_local', 'created_at_utc')
    list_filter = ('rating', 'created_at_local')
    search_fields = ('user__username', 'text')