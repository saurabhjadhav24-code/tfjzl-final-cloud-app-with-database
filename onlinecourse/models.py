```python
# Question model
class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        correct_choices = self.choice_set.filter(is_correct=True)
        selected_correct = correct_choices.filter(
            id__in=selected_ids
        ).count()

        selected_incorrect = self.choice_set.filter(
            is_correct=False,
            id__in=selected_ids
        ).exists()

        return (
            correct_choices.exists()
            and selected_correct == correct_choices.count()
            and not selected_incorrect
        )


# Choice model
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission for Enrollment {self.enrollment.id}"
```
