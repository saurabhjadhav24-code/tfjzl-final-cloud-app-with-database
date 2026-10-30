```python
class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    question_text = models.TextField()
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        correct_ids = set(
            self.choice_set.filter(
                is_correct=True
            ).values_list('id', flat=True)
        )

        selected_correct_ids = set(
            self.choice_set.filter(
                id__in=selected_ids,
                is_correct=True
            ).values_list('id', flat=True)
        )

        return (
            len(correct_ids) > 0
            and correct_ids == selected_correct_ids
        )


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission for Enrollment {self.enrollment.id}"
```
