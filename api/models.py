from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class PrecedentCatalog(models.Model):
    name = models.CharField(max_length=255, unique=True)


class ParticipantManager(models.Manager):
    def compatible(self, user):
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
                    ap.attitude,
                    ap.importance,
                    sq.id,
                    sq.attitude,
                    sq.importance,
                    case
                        when ap.importance > sq.importance
                        then cast(sq.importance as float) / cast(ap.importance as float)
                        else cast(ap.importance as float) / cast(sq.importance as float) 
                    end compatibility
                from {0} p
                join {1} ap on p.id = ap.participant_id
                join {2} a on ap.precedent_id = a.id
                join (
                    select sp.id, sap.precedent_id, sap.attitude, sap.importance
                    from {0} sp
                    join {1} sap on sp.id = sap.participant_id
                    where sp.user_id = {3}
                    ) sq on ap.precedent_id = sq.precedent_id
                where (ap.attitude == sq.attitude) and (p.user_id <> {3} or p.user_id is null)
                order by p.id
                ) int
            group by int.id
            order by cnt desc, weight desc
            limit 20''' \
            .format('api_participant', 'api_precedent', 'api_precedentcatalog', user.id)
        return self.raw(query)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    objects = ParticipantManager()


class Precedent(models.Model):
    ATTITUDE_CHOICES = [
        (0, 'negative'),
        (1, 'positive')
    ]
    precedent = models.ForeignKey(PrecedentCatalog, on_delete=models.CASCADE)
    attitude = models.PositiveSmallIntegerField(choices=ATTITUDE_CHOICES, default=1)
    importance = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    participant = models.ForeignKey(Participant, related_name='precedents', on_delete=models.CASCADE)
