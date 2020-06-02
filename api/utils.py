from django.db.models import Count, Prefetch
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template import loader
import mailer

from .models import Precedent, Participant


def get_popular():
    cached_data = cache.get('popular_precedents', None)
    if cached_data is None:
        q_set = Precedent.objects.values('precedent_id', 'precedent__name') \
            .annotate(count=Count('precedent_id')).order_by('-count')
        cache.set('popular_precedents', list(q_set), 86400)
        cached_data = cache.get('popular_precedents')
    return cached_data


def mail_delivery():
    precedents = get_popular()
    yesterday = timezone.now() - timezone.timedelta(days=1)
    participants = \
        Participant.objects \
            .filter(user__delivery_at__lte=yesterday) \
            .select_related('user') \
            .prefetch_related(Prefetch(
                'precedents',
                queryset=Precedent.objects.all(),
                to_attr='precedents_cache'
            ))[:50]
    participants_list = list(participants)
    precedent_ids = [item['precedent_id'] for item in precedents]
    emails = []
    template = loader.get_template('mail.txt')
    for item in participants_list:
        user_precedents = [value.precedent_id for value in item.precedents_cache]
        to_send = set(precedent_ids) - set(user_precedents)
        precedents_list = [precedents[precedent_ids.index(value)] for key, value in enumerate(to_send) if key < 3]

        emails.append((
            _('Popular precedents'),
            template.render({'precedents_list': precedents_list}),
            settings.DEFAULT_FROM_EMAIL,
            [item.user.email]
        ))
    mailer.send_mass_mail(tuple(emails), fail_silently=False)
