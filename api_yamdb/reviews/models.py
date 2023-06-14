from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model  # Использую пока нет модели User

User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Выберете произведение, чтобы оставить свой отзыв'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст своего отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите свою оценку произведению',
        validators=(
            MinValueValidator(settings.MIN_VALUE_SCORE),
            MaxValueValidator(settings.MAX_VALUE_SCORE)
        ),
        error_messages={
            'validators': (
                f'Оценка должна быть от {settings.MIN_VALUE_SCORE}'
                f'до {settings.MAX_VALUE_SCORE}!'
            ),
        },
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_reviews'
            )
        )

    def __str__(self) -> str:
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self) -> str:
        return self.text
