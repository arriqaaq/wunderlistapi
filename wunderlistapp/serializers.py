from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Folder, Task
from rest_framework.reverse import reverse
from django.utils.translation import ugettext_lazy as _
from datetime import date

User = get_user_model()

class FolderSerializer(serializers.ModelSerializer):
	links = serializers.SerializerMethodField('get_link')
	
	class Meta:
		model = Folder
		fields = ('id', 'name', 'description', 'end', 'links',)

	def get_link(self, obj):
		request = self.context['request']
		return {
			'self': reverse('folder-detail',
				kwargs={'pk': obj.pk},request=request),
			'tasks': reverse('task-list',
				request=request) + '?folder={}'.format(obj.pk),
		}

	#def validate_end(self, attrs, source):
	#	end_date = attrs[source]
	#	new = not self.object
	#	changed = self.object and self.object.end != end_date
	#	if (new or changed) and (end_date < date.today()):
	#		msg = _('End date cannot be in the past.')
	#			raise serializers.ValidationError(msg)
	#	return attrs

class TaskSerializer(serializers.ModelSerializer):
	assigned = serializers.SlugRelatedField(
		slug_field=User.USERNAME_FIELD, required=False,read_only=`True`)
	status_display = serializers.SerializerMethodField('get_status_display1')
	links = serializers.SerializerMethodField('get_link')

	class Meta:
		model = Task
		fields = ('id', 'name', 'status_display','description', 'folder', 'status', 'order',
			'assigned', 'started', 'due', 'completed', 'links',)
	
	def get_status_display1(self, obj):
		return obj.get_status_display()

	def get_link(self, obj):
		request = self.context['request']
		links = {
			'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
			'folder': None,
			'assigned': None
		}
		if obj.folder_id:
				links['folder'] = reverse('folder-detail',
					kwargs={'pk': obj.folder_id}, request=request)
		if obj.assigned:
				links['assigned'] = reverse('user-detail',
					kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
		return links

	#def validate_folder(self, attrs, source):
	#		if self.object and self.object.pk:
	#			if folder != self.object.folder:
	#				if self.object.status == Task.STATUS_DONE:
	#					msg = _('Cannot change the folder of a completed task.')
	#					raise serializers.ValidationError(msg)
	#				if folder and folder.end < date.today():
	#					msg = _('Cannot assign tasks to past folders.')
	#					raise serializers.ValidationError(msg)
	#		else:
	#			if folder and folder.end < date.today():
	#				msg = _('Cannot add tasks to past folders.')
	#				raise serializers.ValidationError(msg)
	#		return attrs

	
class UserSerializer(serializers.ModelSerializer):
	full_name = serializers.CharField(source='get_full_name', read_only=True)
	links = serializers.SerializerMethodField('get_link')

	class Meta:
		model = User
		fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links',)

	def get_link(self, obj):
		request = self.context['request']
		username = obj.get_username()
		return {
			'self': reverse('user-detail',
				kwargs={User.USERNAME_FIELD: username}, request=request),
			'tasks': '{}?assigned={}'.format(
					reverse('task-list', request=request), username)
		}