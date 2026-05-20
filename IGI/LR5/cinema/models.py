import zoneinfo
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def validate_age(value):
    if value < 18:
        raise ValidationError("Возраст должен быть 18 или более лет!")


# =========================================================================
# БАЗОВАЯ АБСТРАКТНАЯ МОДЕЛЬ ДЛЯ ДАТ И ТАЙМЗОН
# =========================================================================
class TimeStampedModel(models.Model):
    """
    Абстрактная модель, автоматически добавляющая поля создания/изменения
    в двух часовых поясах (UTC и Европа/Минск) для всех наследников.
    """
    created_at_utc = models.DateTimeField(null=True, blank=True, verbose_name="Дата создания (UTC)")
    created_at_local = models.DateTimeField(null=True, blank=True, verbose_name="Дата создания (Минск)")
    updated_at_utc = models.DateTimeField(null=True, blank=True, verbose_name="Дата изменения (UTC)")
    updated_at_local = models.DateTimeField(null=True, blank=True, verbose_name="Дата изменения (Минск)")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now_utc = timezone.now()
        minsk_tz = zoneinfo.ZoneInfo("Europe/Minsk")

        # Если запись только создается, фиксируем время создания
        if not self.pk:
            self.created_at_utc = now_utc
            self.created_at_local = now_utc.astimezone(minsk_tz)

        # Время изменения обновляется при каждом сохранении
        self.updated_at_utc = now_utc
        self.updated_at_local = now_utc.astimezone(minsk_tz)

        super().save(*args, **kwargs)


# =========================================================================
# МОДЕЛИ СИСТЕМЫ С ПОДДЕРЖКОЙ ДВУХ ТАЙМЗОН
# =========================================================================

class UserProfile(TimeStampedModel):
    """
    Stores extended user information, specifically managing age requirements, avatars, and phone formats.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(default=18, validators=[validate_age], verbose_name="Возраст")
    photo = models.ImageField(upload_to='users_photos/', blank=True, null=True, verbose_name="Фото профиля")

    phone_regex = RegexValidator(
        regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="Номер телефона должен быть в формате: +375 (XX) XXX-XX-XX"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=19,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Профиль: {self.user.username} (Возраст: {self.age})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class AboutCompany(TimeStampedModel):
    """
    Represents core enterprise information including historical background, logotype, and legal credentials.
    """
    title = models.CharField(max_length=200, verbose_name="Название компании")
    description = models.TextField(verbose_name="Описание/История компании")
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name="Логотип")
    requisites = models.TextField(verbose_name="Реквизиты")

    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"

    def __str__(self):
        return self.title


class NewsArticle(TimeStampedModel):
    """
    Manages promotional and informational announcements featuring mandatory textual summaries and optional visual elements.
    """
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    short_description = models.TextField(verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Полный текст статьи")
    image = models.ImageField(upload_to='news_photos/', blank=True, null=True, verbose_name="Фото новости")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at_utc']  # Сортировка теперь по нашему новому полю создания

    def __str__(self):
        return self.title


class FAQItem(TimeStampedModel):
    """
    Represents frequently asked questions, corporate glossaries, or technical terminologies.
    """
    question = models.CharField(max_length=255, verbose_name="Вопрос / Термин")
    answer = models.TextField(verbose_name="Ответ / Определение")

    class Meta:
        verbose_name = "Вопрос-ответ (FAQ)"
        verbose_name_plural = "Вопросы-ответы (FAQ)"

    def __str__(self):
        return self.question


class ContactEmployee(TimeStampedModel):
    """
    Maintains professional directory information for commercial staff, enforce specific pattern matching for phone numbers.
    """
    full_name = models.CharField(max_length=150, verbose_name="ФИО Сотрудника")
    position = models.CharField(max_length=100, verbose_name="Должность / Выполняемая работа")
    phone = models.CharField(max_length=20, default="+375 (29) 000-00-00", verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    photo = models.ImageField(upload_to="employees/", blank=True, null=True, verbose_name="Фото сотрудника")

    class Meta:
        verbose_name = "Контакт сотрудника"
        verbose_name_plural = "Контакты сотрудников"

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class JobVacancy(TimeStampedModel):
    """
    Handles available corporate roles, structural job prerequisites, and approximate financial packages.
    """
    title = models.CharField(max_length=100, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание обязанностей и требований")
    salary = models.CharField(max_length=50, blank=True, verbose_name="Заработная плата")
    is_active = models.BooleanField(default=True, verbose_name="Вакансии открыта")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title


class PrivacyPolicy(TimeStampedModel):
    """
    Maintains statutory global regulations and internal processing rules regarding user credentials.
    """
    title = models.CharField(max_length=100, default="Политика конфиденциальности")
    content = models.TextField(blank=True, verbose_name="Текст политики безопасности")

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return self.title


class Country(TimeStampedModel):
    """
    Geographical dictionary entity representing jurisdictions of cinematic origin.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название страны")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Genre(TimeStampedModel):
    """
    Cinematographic taxonomy index separating movies into specialized content types.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Movie(TimeStampedModel):
    """
    Core metadata entity representing catalog items with production metrics, runtime details, and multi-relational attributes.
    """
    title_ru = models.CharField(max_length=150, verbose_name="Название (РУС)")
    title_en = models.CharField(max_length=150, verbose_name="Название (ENG)")
    description = models.TextField(verbose_name="Описание фильма")
    duration = models.PositiveIntegerField(verbose_name="Длительность (в минутах)")
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Бюджет ($)")
    rating = models.FloatField(verbose_name="Рейтинг (0.0 - 10.0)")
    poster = models.ImageField(upload_to='posters/', verbose_name="Постер фильма")
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Жанры")
    countries = models.ManyToManyField(Country, verbose_name="Страны производители")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return f"{self.title_ru} ({self.title_en})"


class CinemaHall(TimeStampedModel):
    """
    Physical presentation spaces with dynamic row/seat configuration and automated capacity calculation.
    """
    name = models.CharField(max_length=100, verbose_name="Название/Номер зала")
    rows_count = models.PositiveIntegerField(default=10, verbose_name="Количество рядов")
    seats_per_row = models.PositiveIntegerField(default=10, verbose_name="Количество мест в ряду")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость (мест)", editable=False)

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"

    def save(self, *args, **kwargs):
        # Пересчитываем вместимость
        self.capacity = self.rows_count * self.seats_per_row
        # Вызываем save родительского TimeStampedModel для записи дат/таймзон
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Рядов: {self.rows_count}, Мест в ряду: {self.seats_per_row}, Всего: {self.capacity})"


class Showtime(TimeStampedModel):
    """
    Operational timetables connecting inventory items to structural auditoriums with explicit financial parameters.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes', verbose_name="Фильм")
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='showtimes', verbose_name="Зал")
    start_time = models.DateTimeField(verbose_name="Время начала сеанса")
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена билета (BYN)")

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.movie.title_ru} | {self.hall.name} | {self.start_time.strftime('%d/%m/%Y %H:%M')}"


class StaffProfile(TimeStampedModel):
    """
    Extends user system attributes for corporate human resources, ensuring strict verification against minor personnel.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile', verbose_name="Пользователь")
    position = models.CharField(max_length=100, verbose_name="Должность")
    birth_date = models.DateField(verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def clean(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        if age < 18:
            raise ValidationError({"birth_date": "Сотрудник должен быть совершеннолетним (18+)."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.position}"


class Ticket(TimeStampedModel):
    """
    Transaction records locking unique matrix seating configurations to specific user accounts and commercial sessions.
    """
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='tickets', verbose_name="Сеанс")
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets', verbose_name="Покупатель")
    row = models.PositiveIntegerField(verbose_name="Ряд")
    seat = models.PositiveIntegerField(verbose_name="Место")

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        constraints = [
            models.UniqueConstraint(fields=['showtime', 'row', 'seat'], name='unique_showtime_row_seat')
        ]

    def __str__(self):
        return f"Билет #{self.id} (Ряд {self.row}, Место {self.seat}) на {self.showtime.movie.title_ru}"


class PromoCode(TimeStampedModel):
    """
    Unique voucher codes used to manage programmatic discounts and active financial marketing campaigns.
    """
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    description = models.CharField(max_length=255, verbose_name="Описание скидки/акции")
    is_active = models.BooleanField(default=True, verbose_name="Действующий (Активен)")

    class Meta:
        verbose_name = "Промокод и купон"
        verbose_name_plural = "Промокоды и купоны"

    def __str__(self):
        status = "Активен" if self.is_active else "В архиве"
        return f"{self.code} ({status})"


class Review(TimeStampedModel):
    """
    Holds client evaluations with strict boundaries on numeric scoring, sorting updates in reverse chronological order.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка (1-5)"
    )
    text = models.TextField(verbose_name="Текст отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at_utc']

    def __str__(self):
        return f"Отзыв от {self.user.username} (Оценка: {self.rating})"