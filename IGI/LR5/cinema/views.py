import calendar
from datetime import datetime
import zoneinfo
import requests

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import *


# =========================================================================
# БЛОК ИНТЕРАКТИВНОГО БРОНИРОВАНИЯ, РЕДАКТИРОВАНИЯ И УДАЛЕНИЯ БИЛЕТОВ
# =========================================================================

@login_required
def select_seats_view(request, showtime_id):
    """Страница интерактивного выбора мест для конкретного сеанса"""
    showtime = get_object_or_404(Showtime, id=showtime_id)
    hall = showtime.hall

    # Получаем все уже купленные билеты на этот сеанс в виде словаря {(ряд, место): True}
    booked_tickets = Ticket.objects.filter(showtime=showtime)
    booked_seats = {(t.row, t.seat): True for t in booked_tickets}

    # Генерируем структуру зала динамически на основе его rows_count и seats_per_row
    hall_structure = []
    for r in range(1, hall.rows_count + 1):
        row_seats = []
        for s in range(1, hall.seats_per_row + 1):
            is_booked = (r, s) in booked_seats
            row_seats.append({
                'number': s,
                'is_booked': is_booked
            })
        hall_structure.append({
            'row_number': r,
            'seats': row_seats
        })

    context = {
        'showtime': showtime,
        'movie': showtime.movie,
        'hall': hall,
        'hall_structure': hall_structure,
    }
    return render(request, 'cinema/booking.html', context)


@login_required
def book_ticket_action(request, showtime_id):
    """Обработчик POST-запроса для покупки выбранного места"""
    if request.method == 'POST':
        showtime = get_object_or_404(Showtime, id=showtime_id)

        try:
            row = int(request.POST.get('row'))
            seat = int(request.POST.get('seat'))
        except (ValueError, TypeError):
            messages.error(request, "Некорректно выбраны ряд или место.")
            return redirect('select_seats', showtime_id=showtime.id)

        # Проверяем, не заняли ли это место, пока пользователь думал на схеме
        if Ticket.objects.filter(showtime=showtime, row=row, seat=seat).exists():
            messages.error(request, f"Ряд {row}, Место {seat} уже заняты! Пожалуйста, выберите другое место.")
            return redirect('select_seats', showtime_id=showtime.id)

        try:
            Ticket.objects.create(
                showtime=showtime,
                customer=request.user,
                row=row,
                seat=seat
            )
            messages.success(request,
                             f"Вы успешно забронировали билет на фильм «{showtime.movie.title_ru}»! Ряд {row}, Место {seat}.")
        except Exception:
            messages.error(request, "Произошла непредвиденная ошибка при бронировании. Попробуйте еще раз.")

    return redirect('profile')


@login_required
def delete_ticket_view(request, ticket_id):
    """Удаление (отмена бронирования) билета из личного кабинета"""
    ticket = get_object_or_404(Ticket, id=ticket_id, customer=request.user)
    movie_title = ticket.showtime.movie.title_ru
    ticket.delete()
    messages.success(request, f"Билет на фильм «{movie_title}» успешно отменен.")
    return redirect('profile')


@login_required
def edit_ticket_seats_view(request, ticket_id):
    """Страница и обработчик изменения места для уже оформленного билета"""
    ticket = get_object_or_404(Ticket, id=ticket_id, customer=request.user)
    showtime = ticket.showtime
    hall = showtime.hall

    # Собираем занятые места другими людьми (текущее место самого пользователя исключаем, чтобы его можно было перевыбрать)
    booked_tickets = Ticket.objects.filter(showtime=showtime).exclude(id=ticket.id)
    booked_seats = {(t.row, t.seat): True for t in booked_tickets}

    if request.method == 'POST':
        try:
            new_row = int(request.POST.get('row'))
            new_seat = int(request.POST.get('seat'))
        except (ValueError, TypeError):
            messages.error(request, "Некорректный выбор новых мест.")
            return redirect('edit_ticket', ticket_id=ticket.id)

        if (new_row, new_seat) in booked_seats:
            messages.error(request, f"Ряд {new_row}, Место {new_seat} уже заняты кем-то другим!")
        else:
            ticket.row = new_row
            ticket.seat = new_seat
            ticket.save()
            messages.success(request, f"Место успешно изменено на Ряд {new_row}, Место {new_seat}!")
            return redirect('profile')

    # Формируем сетку зала для страницы редактирования
    hall_structure = []
    for r in range(1, hall.rows_count + 1):
        row_seats = []
        for s in range(1, hall.seats_per_row + 1):
            is_booked = (r, s) in booked_seats
            is_current = (r == ticket.row and s == ticket.seat)
            row_seats.append({
                'number': s,
                'is_booked': is_booked,
                'is_current': is_current
            })
        hall_structure.append({
            'row_number': r,
            'seats': row_seats
        })

    return render(request, 'cinema/edit_ticket.html', {
        'ticket': ticket,
        'showtime': showtime,
        'movie': showtime.movie,
        'hall_structure': hall_structure
    })


# =========================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И СЕРВИСЫ
# =========================================================================

def is_staff_or_admin(user):
    return user.is_superuser or hasattr(user, 'staff_profile')


def get_movie_data_from_api(movie_title):
    api_key = "d91bc258"
    safe_title = str(movie_title).strip().replace(' ', '+')
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={safe_title}"

    default_data = {
        'imdb_rating': 'N/A',
        'director': 'Не указан',
        'year': '—'
    }

    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    'imdb_rating': data.get('imdbRating', 'N/A'),
                    'director': data.get('Director', 'Не указан'),
                    'year': data.get('Year', '—')
                }
    except requests.RequestException:
        pass

    return default_data


# =========================================================================
# ОСНОВНЫЕ ПРЕДСТАВЛЕНИЯ (VIEWS) СИСТЕМЫ
# =========================================================================

def dashboard_view(request):
    reviews = Review.objects.all()
    total_reviews = reviews.count()

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 2)

    ratings_list = list(reviews.values_list('rating', flat=True))
    ratings_list = sorted(list(ratings_list))

    if total_reviews > 0:
        mid = total_reviews // 2
        if total_reviews % 2 == 0:
            median_rating = (ratings_list[mid - 1] + ratings_list[mid]) / 2
        else:
            median_rating = ratings_list[mid]
    else:
        median_rating = 0

    if total_reviews > 0:
        mode_data = reviews.values('rating').annotate(count=Count('rating')).order_by('-count').first()
        mode_rating = mode_data['rating'] if mode_data else 0
    else:
        mode_rating = 0

    popular_genre_data = Movie.objects.values('genres__name').annotate(movie_count=Count('id')).order_by(
        '-movie_count').first()
    top_genre = popular_genre_data['genres__name'] if popular_genre_data and popular_genre_data[
        'genres__name'] else "Нет данных"

    total_sales_sim = Showtime.objects.aggregate(total_price=Sum('ticket_price'))['total_price'] or 0

    movies_alphabetical = Movie.objects.order_by('title_ru')

    rating_counts = []
    for i in range(1, 6):
        count = reviews.filter(rating=i).count()
        rating_counts.append(count)

    utc_now = datetime.now(zoneinfo.ZoneInfo("UTC"))
    user_tz_name = "Europe/Minsk"
    user_now = datetime.now(zoneinfo.ZoneInfo(user_tz_name))

    current_date_formatted = user_now.strftime("%d/%m/%Y")
    html_cal = calendar.HTMLCalendar(calendar.MONDAY).formatmonth(user_now.year, user_now.month)

    context = {
        'avg_rating': avg_rating,
        'median_rating': median_rating,
        'mode_rating': mode_rating,
        'total_reviews': total_reviews,
        'total_sales_sim': total_sales_sim,
        'top_genre': top_genre,
        'movies_alphabetical': movies_alphabetical,
        'rating_counts': rating_counts,
        'current_date_formatted': current_date_formatted,
        'utc_time': utc_now.strftime("%d/%m/%Y %H:%M:%S UTC"),
        'user_time': user_now.strftime("%d/%m/%Y %H:%M:%S") + f" ({user_tz_name})",
        'html_calendar': html_cal,
    }
    return render(request, 'cinema/dashboard.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')

        if form.is_valid():
            if not age or int(age) < 18:
                messages.error(request, "Регистрация доступна только лицам старше 18 лет.")
                return render(request, 'cinema/register.html', {'form': form})

            user = form.save(commit=False)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            user.save()

            user.profile.age = int(age)
            if photo:
                user.profile.photo = photo
            if phone:
                user.profile.phone = phone
            user.profile.save()

            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'cinema/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'cinema/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def index_view(request):
    latest_news = NewsArticle.objects.order_by('-created_at_local').first()
    return render(request, 'cinema/index.html', {'latest_news': latest_news})


def about_view(request):
    company_info = AboutCompany.objects.first()
    return render(request, 'cinema/about.html', {'company_info': company_info})


def movies_list_view(request):
    movies = Movie.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(title_ru__icontains=search_query)

    sort_by = request.GET.get('sort', 'title_ru')
    if sort_by in ['title_ru', '-rating', 'duration']:
        movies = movies.order_by(sort_by)

    for movie in movies:
        api_data = get_movie_data_from_api(movie.title_en)
        movie.imdb_rating = api_data['imdb_rating']
        movie.director = api_data['director']
        movie.release_year = api_data['year']

    active_promos = PromoCode.objects.filter(is_active=True)
    archived_promos = PromoCode.objects.filter(is_active=False)

    context = {
        'movies': movies,
        'active_promos': active_promos,
        'archived_promos': archived_promos,
        'search_query': search_query,
        'sort_by': sort_by
    }
    return render(request, 'cinema/movies_list.html', context)


def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = movie.showtimes.all()
    return render(request, 'cinema/movie_detail.html', {'movie': movie, 'showtimes': showtimes})


@login_required
@user_passes_test(is_staff_or_admin)
def news_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        NewsArticle.objects.create(title=title, short_description=short_description, content=content, image=image)
        return redirect('index')
    return render(request, 'cinema/news_form.html', {'action': 'Создать'})


@login_required
@user_passes_test(is_staff_or_admin)
def news_update_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.short_description = request.POST.get('short_description')
        article.content = request.POST.get('content')
        if request.FILES.get('image'):
            article.image = request.FILES.get('image')
        article.save()
        return redirect('index')
    return render(request, 'cinema/news_form.html', {'article': article, 'action': 'Сохранить изменения'})


@login_required
@user_passes_test(is_staff_or_admin)
def news_delete_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('index')
    return render(request, 'cinema/news_confirm_delete.html', {'article': article})


def contacts_view(request):
    employees = ContactEmployee.objects.all()
    context = {
        'employees': employees,
        'address': 'г. Минск, пр-т Победителей, д. 9',
        'phone': '+375 (29) 111-22-33'
    }
    return render(request, 'cinema/contacts.html', context)


def reviews_view(request):
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm(instance=user_review)

    all_reviews = Review.objects.all().order_by('-created_at')
    if user_review:
        all_reviews = all_reviews.exclude(id=user_review.id)

    return render(request, 'cinema/reviews.html', {
        'reviews': all_reviews,
        'user_review': user_review,
        'form': form
    })


import io
import base64
import matplotlib

matplotlib.use('Agg')  # Деактивируем GUI-интерфейс для потокобезопасной работы в вебе
import matplotlib.pyplot as plt

from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from .models import Movie, Ticket, Review, UserProfile, Showtime


@login_required
def profile_view(request):
    """Личный кабинет пользователя с его данными, историей билетов или панелью администратора"""
    user_profile = getattr(request.user, 'profile', None)

    # Контекст по умолчанию
    context = {
        'profile': user_profile,
        'is_employee': request.user.is_staff or request.user.is_superuser,
    }

    # ЕСЛИ ПОЛЬЗОВАТЕЛЬ — АДМИН ИЛИ СОТРУДНИК, СОБИРАЕМ РАСШИРЕННУЮ СТАТИСТИКУ
    if context['is_employee']:
        # 1. Список клиентов в алфавитном порядке (по username)
        clients_alphabetical = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')

        # 2. Список фильмов в алфавитном порядке и общая сумма продаж по каждому
        # Считаем сумму продаж: Количество купленных билетов * Цена билета за сеанс
        movies_alphabetical = Movie.objects.annotate(
            total_sales=Sum('showtimes__tickets__showtime__ticket_price')
        ).order_by('title_ru')

        # Общая сумма продаж по всему кинотеатру
        total_sales_sum = Ticket.objects.aggregate(
            total=Sum('showtime__ticket_price')
        )['total'] or 0

        # 3. Статистические показатели по возрасту клиентов (Среднее и Медиана)
        active_ages = list(UserProfile.objects.filter(
            user__is_staff=False, user__is_superuser=False
        ).values_list('age', flat=True))
        active_ages = sorted([age for age in active_ages if age is not None])

        total_clients = len(active_ages)
        avg_age = round(sum(active_ages) / total_clients, 1) if total_clients > 0 else 0

        if total_clients > 0:
            mid = total_clients // 2
            median_age = (active_ages[mid - 1] + active_ages[mid]) / 2 if total_clients % 2 == 0 else active_ages[mid]
        else:
            median_age = 0

        # 4. Самый популярный фильм (по количеству купленных билетов)
        top_movie_by_tickets = Movie.objects.annotate(
            tickets_count=Count('showtimes__tickets')
        ).order_by('-tickets_count').first()

        # Самый прибыльный фильм (по сумме сборов)
        top_movie_by_revenue = Movie.objects.annotate(
            revenue=Sum('showtimes__tickets__showtime__ticket_price')
        ).order_by('-revenue').first()

        # 5. Метрики по суммам покупок билетов (Среднее, Мода, Медиана стоимостей проданных билетов)
        ticket_prices = list(Ticket.objects.values_list('showtime__ticket_price', flat=True))
        ticket_prices = sorted([float(p) for p in ticket_prices if p is not None])
        total_tickets = len(ticket_prices)

        avg_ticket_cost = round(sum(ticket_prices) / total_tickets, 2) if total_tickets > 0 else 0

        # Медиана цен
        if total_tickets > 0:
            mid_t = total_tickets // 2
            median_ticket_cost = (ticket_prices[mid_t - 1] + ticket_prices[mid_t]) / 2 if total_tickets % 2 == 0 else \
            ticket_prices[mid_t]
        else:
            median_ticket_cost = 0

        # Мода цен билетов
        if total_tickets > 0:
            mode_data = Ticket.objects.values('showtime__ticket_price').annotate(
                count=Count('id')
            ).order_by('-count').first()
            mode_ticket_cost = mode_data['showtime__ticket_price'] if mode_data else 0
        else:
            mode_ticket_cost = 0

        # =========================================================================
        # ПОСТРОЕНИЕ ГРАФИКОВ ЧЕРЕЗ PYTHON (MATPLOTLIB) БЕЗ JS
        # =========================================================================
        chart_sales = ""
        chart_reviews = ""

        if total_tickets > 0:
            # График 1: Распределение прибыли по фильмам (Столбчатая диаграмма)
            plt.figure(figsize=(6, 4))
            movie_titles = [m.title_ru[:12] + '...' if len(m.title_ru) > 12 else m.title_ru for m in
                            movies_alphabetical]
            movie_revenues = [float(m.total_sales or 0) for m in movies_alphabetical]

            plt.bar(movie_titles, movie_revenues, color='#1890ff', alpha=0.8)
            plt.title('Прибыль по фильмам (BYN)', fontsize=12, fontweight='bold', pad=15)
            plt.xticks(rotation=20, ha='right')
            plt.ylabel('Сумма (BYN)')
            plt.tight_layout()

            # Конвертируем график в Base64 строку
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            chart_sales = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()

            # График 2: Распределение оценок в отзывах
            reviews = Review.objects.all()
            rating_counts = [reviews.filter(rating=i).count() for i in range(1, 6)]

            plt.figure(figsize=(6, 4))
            plt.bar(['1 ★', '2 ★', '3 ★', '4 ★', '5 ★'], rating_counts, color='#52c41a', alpha=0.8)
            plt.title('Распределение оценок пользователей', fontsize=12, fontweight='bold', pad=15)
            plt.ylabel('Количество отзывов')
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150)
            buffer.seek(0)
            chart_reviews = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()

        # Добавляем все расчетные данные для админа в контекст
        context.update({
            'clients_alphabetical': clients_alphabetical,
            'movies_alphabetical': movies_alphabetical,
            'total_sales_sum': total_sales_sum,
            'avg_age': avg_age,
            'median_age': median_age,
            'top_movie_by_tickets': top_movie_by_tickets,
            'top_movie_by_revenue': top_movie_by_revenue,
            'avg_ticket_cost': avg_ticket_cost,
            'median_ticket_cost': median_ticket_cost,
            'mode_ticket_cost': mode_ticket_cost,
            'chart_sales': chart_sales,
            'chart_reviews': chart_reviews,
        })
    else:
        # Для обычного клиента просто берем его билеты
        context['tickets'] = Ticket.objects.filter(customer=request.user).select_related('showtime__movie',
                                                                                         'showtime__hall')
    return render(request, 'cinema/profile.html', context)