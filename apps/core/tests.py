from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from apps.core.admin import UserAdminForm, CustomUserCreationForm, ensure_group_permissions
from apps.core.models import PageContent
from apps.core.templatetags.page_editor import page_val, page_block, edit_btn

class UserAccessControlTestCase(TestCase):
    def setUp(self):
        ensure_group_permissions()

    def test_custom_user_creation_form_syncs_groups(self):
        # Create a new user with CRM access
        data = {
            'username': 'crm_admin_user',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'access_crm': True,
            'access_ai': False,
            'access_marketing': False,
            'access_operations': False,
            'access_security': False,
        }
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        
        user = form.save()
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        # Verify the user is in the CRM & Sales Managers group
        user_groups = user.groups.values_list('name', flat=True)
        self.assertIn('CRM & Sales Managers', user_groups)
        self.assertNotIn('AI Assistant Managers', user_groups)

    def test_user_admin_form_updates_groups(self):
        # Create user
        user = User.objects.create_user(username='test_user', password='password123')
        self.assertFalse(user.is_staff)
        
        # Open form to edit user
        data = {
            'username': 'test_user',
            'access_crm': False,
            'access_ai': True,
            'access_marketing': False,
            'access_operations': True,
            'access_security': False,
        }
        form = UserAdminForm(data=data, instance=user)
        self.assertTrue(form.is_valid(), form.errors)
        
        updated_user = form.save()
        self.assertTrue(updated_user.is_staff)
        
        # Verify groups updated
        user_groups = updated_user.groups.values_list('name', flat=True)
        self.assertIn('AI Assistant Managers', user_groups)
        self.assertIn('Operations & Careers Managers', user_groups)
        self.assertNotIn('CRM & Sales Managers', user_groups)
        
        # Now remove operations access
        data['access_operations'] = False
        form2 = UserAdminForm(data=data, instance=updated_user)
        self.assertTrue(form2.is_valid(), form2.errors)
        
        final_user = form2.save()
        user_groups_final = final_user.groups.values_list('name', flat=True)
        self.assertIn('AI Assistant Managers', user_groups_final)
        self.assertNotIn('Operations & Careers Managers', user_groups_final)

class ContextProcessorTestCase(TestCase):
    def test_admin_available_apps_context_processor(self):
        from django.test import RequestFactory
        from apps.core.context_processors import admin_available_apps
        
        factory = RequestFactory()
        
        # 1. Non-admin page request
        request = factory.get('/')
        context = admin_available_apps(request)
        self.assertEqual(context, {})
        
        # 2. Admin page request (authenticated superuser)
        request = factory.get('/admin/auth/user/')
        superuser = User.objects.create_superuser(username='super', email='s@test.com', password='password123')
        request.user = superuser
        
        context = admin_available_apps(request)
        self.assertIn('available_apps', context)
        self.assertTrue(len(context['available_apps']) > 0)


class PageContentCMSTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(username='super', email='s@test.com', password='password123')
        self.regular_user = User.objects.create_user(username='regular', email='r@test.com', password='password123')

    def test_page_val_seeding_and_retrieval(self):
        # 1. Page val for key that does not exist should create it with default
        context = {'request': self.factory.get('/')}
        val = page_val(context, 'test_page', 'test_sec', 'test_key', default='Hello World', content_type='text')
        self.assertEqual(val, 'Hello World')
        
        # Verify db record was created
        record = PageContent.objects.get(page='test_page', section='test_sec', key='test_key')
        self.assertEqual(record.text_value, 'Hello World')
        self.assertEqual(record.content_type, 'text')
        
        # 2. Retrieve existing record with different default (should return db value)
        val2 = page_val(context, 'test_page', 'test_sec', 'test_key', default='New Default')
        self.assertEqual(val2, 'Hello World')

    def test_page_block_rendering(self):
        # 1. Anonymous / Non-staff user should get raw content
        request = self.factory.get('/')
        request.user = self.regular_user
        context = {'request': request}
        
        val = page_block(context, 'test_page', 'test_sec', 'test_block_key', default='Welcome Info', content_type='text')
        self.assertEqual(val, 'Welcome Info')
        
        # 2. Staff user should get wrapped content with edit link
        request_staff = self.factory.get('/')
        request_staff.user = self.superuser
        context_staff = {'request': request_staff}
        
        val_staff = page_block(context_staff, 'test_page', 'test_sec', 'test_block_key', default='Welcome Info', content_type='text')
        self.assertIn('Welcome Info', val_staff)
        self.assertIn('group-hover/cms-block', val_staff)
        self.assertIn('core/pagecontent/', val_staff)

    def test_edit_btn_rendering(self):
        # 1. Non-staff user gets empty string
        request = self.factory.get('/')
        request.user = self.regular_user
        context = {'request': request}
        self.assertEqual(edit_btn(context, 'test_page', 'test_sec', 'test_block_key'), '')
        
        # 2. Staff user gets edit button link if PageContent exists
        request_staff = self.factory.get('/')
        request_staff.user = self.superuser
        context_staff = {'request': request_staff}
        
        # Seed record first
        PageContent.objects.create(page='test_page', section='test_sec', key='test_btn_key', text_value='val')
        btn_html = edit_btn(context_staff, 'test_page', 'test_sec', 'test_btn_key')
        self.assertIn('core/pagecontent/', btn_html)
        self.assertIn('Edit', btn_html)



