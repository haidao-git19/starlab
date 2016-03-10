# coding:utf8
from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    (1, '加密站(线上)'),
    (2, '加密站(建设)'),
    (3, '框架站'),
)
class Receiver(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    real_time = models.DateTimeField(db_column='REAL_TIME', blank=True, null=True)  # Field name made lowercase.
    rec_sn = models.CharField(db_column='REC_SN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rec_type = models.CharField(db_column='REC_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rec_exp_date = models.CharField(db_column='REC_EXP_DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rec_hardware = models.CharField(db_column='REC_HARDWARE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mb_type = models.CharField(db_column='MB_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mb_sn = models.CharField(db_column='MB_SN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mb_mode = models.CharField(db_column='MB_MODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mb_hardware = models.CharField(db_column='MB_HARDWARE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    voltage_in = models.CharField(db_column='VOLTAGE_IN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    voltage_out = models.CharField(db_column='VOLTAGE_OUT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rec_mem = models.CharField(db_column='REC_MEM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    u_men = models.CharField(db_column='U_MEN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sd_men = models.CharField(db_column='SD_MEN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rec_temp = models.CharField(db_column='REC_TEMP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    start_time = models.DateField(db_column='START_TIME', blank=True, null=True)  # Field name made lowercase.
    shutdown_time = models.DateField(db_column='SHUTDOWN_TIME', blank=True, null=True)  # Field name made lowercase.
    antenna_type = models.CharField(db_column='ANTENNA_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    antenna_height = models.CharField(db_column='ANTENNA_HEIGHT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    antenna_1_gain = models.CharField(db_column='ANTENNA_1_GAIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    antenna_2_gain = models.CharField(db_column='ANTENNA_2_GAIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    work_mode = models.CharField(db_column='WORK_MODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sat_num = models.CharField(db_column='SAT_NUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ant_angle = models.CharField(db_column='ANT_ANGLE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='LATITUDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='LONGITUDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    solution_status = models.CharField(db_column='SOLUTION_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    diff_schema = models.CharField(db_column='DIFF_SCHEMA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    net_trans_num = models.CharField(db_column='NET_TRANS_NUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    record_num = models.CharField(db_column='RECORD_NUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    com_trans_num = models.CharField(db_column='COM_TRANS_NUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    elevation = models.CharField(db_column='ELEVATION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    enabled = models.TextField(blank=True, null=True)  # This field type is a guess.
    updatetime = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=1, blank=True, null=True)
    category_id = models.IntegerField(choices=CATEGORY_CHOICES, blank=True, null=True)
    station_cnname = models.CharField(max_length=20, blank=True, null=True)
    station_code = models.CharField(max_length=20, blank=True, null=True)
    station_ip = models.CharField(max_length=20, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    station_pm = models.CharField(max_length=20, blank=True, null=True)
    station_agent_owner = models.CharField(max_length=20, blank=True, null=True)
    station_agent_contact = models.CharField(max_length=20, blank=True, null=True)
    station_industry = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receiver'

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('amap:details', args=[str(self.id)])


# class Receiver_extend(models.Model):
#     receiver = models.OneToOneField(Receiver)