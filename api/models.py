from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import FilteredRelation, Q, Subquery
from django.utils.translation import gettext_lazy as _


# Create your models here.
class PrecedentCatalog(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ParticipantManager(models.Manager):
    def compatible_raw(self, user):
        query = '''
            select int.id,
                int.name,
                sum(int.compatibility),
                count(int.id) as cnt,
                round(sum(int.compatibility) / cast(count(int.id) as real) * 100) as weight
            from (
                select p.id   as id,
                    p.name as  name,
                    a.name,
                    ap.importance,
                    sq.id,
                    sq.importance,
                    case
                        when abs(ap.importance) > abs(sq.importance)
                        then cast(sq.importance as float) / cast(ap.importance as float)
                        else cast(ap.importance as float) / cast(sq.importance as float) 
                    end compatibility
                from {0} p
                join {1} ap on p.id = ap.participant_id
                join {2} a on ap.precedent_id = a.id
                join (
                    select sp.id, sap.precedent_id, sap.importance
                    from {0} sp
                    join {1} sap on sp.id = sap.participant_id
                    where sp.user_id = {3}
                    ) sq on ap.precedent_id = sq.precedent_id
                where (p.user_id <> {3} or p.user_id is null)
                order by p.id
                ) int
            group by int.id
            order by weight desc
            limit 20''' \
            .format('api_participant', 'api_precedent', 'api_precedentcatalog', user.id)
        return self.raw(query)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    # Null=true т.к. в фикстурах недостаточно данных для создания связанных пользователей
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    objects = ParticipantManager()

    def __str__(self):
        return self.name


def importance_validator(value):
    if not abs(value) in list(range(1,11)):
        raise ValidationError(_('Importance value %(value)s not in allowed range'), params={'value': value})


class Precedent(models.Model):
    precedent = models.ForeignKey(PrecedentCatalog, on_delete=models.CASCADE)
    importance = models.SmallIntegerField(validators=[importance_validator])
    participant = models.ForeignKey(Participant, related_name='precedents', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['precedent', 'participant']

    def __str__(self):
        return '{}: {}'.format(self.participant, self.precedent.name)
