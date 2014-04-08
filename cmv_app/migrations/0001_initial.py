# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table(u'cmv_app_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'cmv_app', ['Region'])

        # Adding model 'Search'
        db.create_table(u'cmv_app_search', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('vehicle_make', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('vehicle_model', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('extra_keywords', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('max_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('min_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('max_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('min_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('pic_only', self.gf('django.db.models.fields.BooleanField')()),
            ('search_title_only', self.gf('django.db.models.fields.BooleanField')()),
            ('seller_type', self.gf('django.db.models.fields.CharField')(default='a', max_length=1)),
        ))
        db.send_create_signal(u'cmv_app', ['Search'])

        # Adding M2M table for field regions on 'Search'
        m2m_table_name = db.shorten_name(u'cmv_app_search_regions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'cmv_app.search'], null=False)),
            ('region', models.ForeignKey(orm[u'cmv_app.region'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'region_id'])

        # Adding model 'Posting'
        db.create_table(u'cmv_app_posting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmv_app.Region'])),
            ('posting_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('vehicle_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('vehicle_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cmv_app', ['Posting'])

        # Adding M2M table for field search on 'Posting'
        m2m_table_name = db.shorten_name(u'cmv_app_posting_search')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('posting', models.ForeignKey(orm[u'cmv_app.posting'], null=False)),
            ('search', models.ForeignKey(orm[u'cmv_app.search'], null=False))
        ))
        db.create_unique(m2m_table_name, ['posting_id', 'search_id'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table(u'cmv_app_region')

        # Deleting model 'Search'
        db.delete_table(u'cmv_app_search')

        # Removing M2M table for field regions on 'Search'
        db.delete_table(db.shorten_name(u'cmv_app_search_regions'))

        # Deleting model 'Posting'
        db.delete_table(u'cmv_app_posting')

        # Removing M2M table for field search on 'Posting'
        db.delete_table(db.shorten_name(u'cmv_app_posting_search'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cmv_app.posting': {
            'Meta': {'object_name': 'Posting'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'posting_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cmv_app.Region']"}),
            'search': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'p_s+'", 'symmetrical': 'False', 'to': u"orm['cmv_app.Search']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vehicle_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vehicle_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'cmv_app.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'cmv_app.search': {
            'Meta': {'object_name': 'Search'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'extra_keywords': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pic_only': ('django.db.models.fields.BooleanField', [], {}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'s_r+'", 'symmetrical': 'False', 'to': u"orm['cmv_app.Region']"}),
            'search_title_only': ('django.db.models.fields.BooleanField', [], {}),
            'seller_type': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vehicle_make': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'vehicle_model': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cmv_app']