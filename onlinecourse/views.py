```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Enrollment, Submission, Choice
import logging

logger = logging.getLogger(__name__)


def registration_request(request):
    context = {}

    if request.method == 'GET':
        return render(
            request,
            'onlinecourse/user_registration_bootstrap.html',
            context
        )

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = User.objects.filter(username=username).exists()

        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect('onlinecourse:index')

        context['message'] = 'User already exists.'
        return render(
            request,
            'onlinecourse/user_registration_bootstrap.html',
            context
        )


def login_request(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')

        context['message'] = 'Invalid username or password.'
        return render(
            request,
            'onlinecourse/user_login_bootstrap.html',
            context
        )

    return render(
        request,
        'onlinecourse/user_login_bootstrap.html',
        context
    )


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    if user.is_authenticated:
        return Enrollment.objects.filter(
            user=user,
            course=course
        ).exists()

    return False


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]

        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)

        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if user.is_authenticated:
        is_enrolled = check_if_enrolled(user, course)

        if not is_enrolled:
            Enrollment.objects.create(
                user=user,
                course=course,
                mode='honor'
            )

            course.total_enrollment += 1
            course.save()

    return HttpResponseRedirect(
        reverse(
            viewname='onlinecourse:course_details',
            args=(course.id,)
        )
    )


def extract_answers(request):
    submitted_answers = []

    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]

            try:
                choice_id = int(value)
                submitted_answers.append(choice_id)
            except (ValueError, TypeError):
                continue

    return submitted_answers


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')

    if request.method != 'POST':
        return redirect(
            'onlinecourse:course_details',
            course_id=course.id
        )

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_answers = extract_answers(request)

    for choice_id in selected_answers:
        choice = get_object_or_404(
            Choice,
            pk=choice_id
        )

        submission.choices.add(choice)

    return redirect(
        'onlinecourse:show_exam_result',
        submission_id=submission.id
    )


def show_exam_result(request, submission_id):
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user
    )

    course = submission.enrollment.course

    selected_ids = list(
        submission.choices.values_list('id', flat=True)
    )

    total_score = 0
    question_results = []

    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            is_correct = question.is_get_score(selected_ids)

            if is_correct:
                total_score += question.grade

            question_results.append({
                'question': question,
                'is_correct': is_correct,
                'selected_choices': question.choice_set.filter(
                    id__in=selected_ids
                ),
                'correct_choices': question.choice_set.filter(
                    is_correct=True
                ),
            })

    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'question_results': question_results,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
```
