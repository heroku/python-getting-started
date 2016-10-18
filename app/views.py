from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import redirect
from teams.models import Team, JoinRequest
from django.core.mail import send_mail
from .models import Alert

from app.models import Organization, OrganizationMember, Token, Profile, OrganizationInvitation
from teams.models import Team, Member, Role
from app.forms import OrgSignUpForm, SettingsForm, UserSignUpForm, SignInForm
from teamedup import settings

import json, datetime


@login_required
def index(request):
    try:
        organization = Organization.get_single_by_user(request.user)
    except Organization.DoesNotExist:
        messages.add_message(request, messages.WARNING, 'You\'re not assigned to any organizations')
        organization = None
        # return redirect('/app/')

    if organization is not None:
        teams = Team.objects.filter(organization=organization)
        myteams = [member.team for member in request.user.member_set.filter(team_id__in=[t.pk for t in teams])]
        otherteams = [team for team in teams if team not in myteams]

    return render(request, 'app/home.html', locals())


def login_view(request):
    next = request.GET.get('next')
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Your have signed in successfully'))
                return redirect('/app/')
    return render(request, 'app/login.html', locals())


@login_required
def edit_settings(request):
    if not hasattr(request.user, 'profile'):
        # TODO: remove this block before release
        _profile = Profile(user=request.user).save()

    organizations = [membership.organization for membership in OrganizationMember.objects.filter(user=request.user, is_owner=True)]

    initial = {
        'name': request.user.profile.name,
        'email': request.user.email,
        'bio': request.user.profile.bio,
        'city': request.user.profile.city,
        'country': request.user.profile.country
    }

    form = SettingsForm(initial=initial)
    if request.method == 'POST':
        form = SettingsForm(request.POST, initial=initial)
        form.set_user(request.user)
        if form.is_valid():
            if request.FILES.get('userpic'):
                request.user.profile.userpic =  request.FILES.get('userpic')
            request.user.profile.name = form.cleaned_data.get('name')
            request.user.profile.city = form.cleaned_data.get('city')
            request.user.profile.country = form.cleaned_data.get('country')
            request.user.profile.bio = form.cleaned_data.get('bio')
            request.user.profile.save()
            # TODO: if email was updated -> mark user account is_active=False and send activation link
            password = form.cleaned_data.get('password')
            if password != '':
                request.user.set_password(password)
                request.user.save()
            messages.add_message(request, messages.SUCCESS, _('Your account was updated successfully'))
            return redirect(reverse('index'))
    return render(request, 'app/settings.html', locals())


def signup(request):
    form = OrgSignUpForm()
    if request.method == 'POST':
        form = OrgSignUpForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data.get('email'), username=form.cleaned_data.get('email'))
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            _profile = Profile(user=user).save()
            org = Organization(name=form.cleaned_data.get('organization_name'))
            org.save()
            _orgmem = OrganizationMember(user=user, is_owner=True, organization=org).save()
            token = Token(user=user, type='signup')
            token.save()
            link = request.build_absolute_uri(reverse('activate-account', args=[token.token]))

            print('Activation link: %s' % (link))

            send_mail('Account activation', settings.ACCOUNT_ACTIVATION_EMAIL % (org.name, link,),
                      'noreply@teamedup.com', [user.email, ])
            messages.add_message(request, messages.SUCCESS,
                                 _('Please click the activation link which was sent to your email'))
            _user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if _user is not None: # TODO: only sign in users which activated their account
                login(request, _user)
                return redirect('/app/')
            return redirect('/')
    return render(request, 'app/signup.html', locals())


def join_organization(request, token):
    try:
        inv = OrganizationInvitation.objects.get(token=token, expired=False)
    except OrganizationInvitation.DoesNotExist:
        raise Http404

    form = UserSignUpForm()
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        form.set_email(inv.email)
        if form.is_valid():
            inv.expire()
            user = User()
            user.username = inv.email
            user.email = inv.email
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = True
            user.save()
            Profile(user=user).save()
            OrganizationMember(user=user, organization=inv.organization).save()
            _user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if _user is not None:
                login(request, _user)
                return redirect('/app/')
    return render(request, 'app/join-organization.html', locals())


def activate_account(request, token):
    try:
        token = Token.objects.get(token=token, expired=False, type='signup')
    except Token.DoesNotExist:
        raise Http404

    token.user.is_active = True
    token.user.save()
    messages.add_message(request, messages.SUCCESS, _('Your account is now active'))
    return redirect('login_view')


def sign_out(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have successfully logged out'))
    return redirect(reverse('login_view'))

def searchpeople(request):
    organization = Organization.get_single_by_user(request.user)
    peoples = [membership.user for membership in organization.members]
    teams = organization.team_set.all()

    return render(request, 'app/people.html', locals())

@login_required
def notifications_page(request):
    return render(request, 'app/notifications.html', locals())

def getnotifications(request):
    notifications = []

    team_invites = request.user.inviteds.all().filter(status="created")
    for team_invite in team_invites:
        notification = {
            'type': 'team_invite',
            'created_at': team_invite.created_at.strftime('%m-%d-%Y %H:%M'),
            'object': team_invite.to_dict()
        }
        notifications.append(notification)

    teams_owned = [member.team.pk for member in request.user.member_set.all().filter(is_owner=True)]
    team_joinrequests = JoinRequest.objects.all().filter(team__id__in=teams_owned).filter(status="created")
    for team_joinrequest in team_joinrequests:
        notification = {
            'type': 'team_join',
            'created_at': team_joinrequest.created_at.strftime('%m-%d-%Y %H:%M'),
            'object': team_joinrequest.to_dict()
        }
        notifications.append(notification)

    return HttpResponse(json.dumps({'entries': notifications, 'total': 0}), content_type='application/json')


@login_required
def user_page(request, user_id):
    member = get_object_or_404(User, pk=user_id)
    memberships = Member.objects.filter(user=member)
    current_roles = []
    past_roles = []
    for ms in memberships:
        current_roles += ms.role.filter(end_date__gt=datetime.datetime.now())
        past_roles += ms.role.filter(end_date__lte=datetime.datetime.now())
    # TODO: validation required
    teams = [membership.team for membership in Member.objects.filter(user=member)]
    return render(request, 'app/user_page.html', locals())

