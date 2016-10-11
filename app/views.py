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
import json
from django.core.mail import send_mail
from .models import Alert

from app.models import Organization, OrganizationMember, Token, Profile, OrganizationInvitation
from teams.models import Team
from app.forms import OrgSignUpForm, SettingsForm, UserSignUpForm, SignInForm
from teamedup import settings


@login_required
def index(request):
    teams = Team.objects.all()
    myteams = [member.team for member in request.user.member_set.all()]
    otherteams = [team for team in teams if team not in myteams]
    context = {
        'teams': teams,
        'myteams': myteams,
        'otherteams': otherteams,
    }
    return render(request, 'app/home.html', context)


def login_user(request):
    # logout(request)
    username = password = ''

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/app')
            else:
                return HttpResponse("Please check your username or password and try again.")
        else:
            return HttpResponse("Please check your username or password and try again.")
    return HttpResponse()


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
        'email': request.user.email
    }

    form = SettingsForm(initial=initial)
    if request.method == 'POST':
        form = SettingsForm(request.POST, initial=initial)
        form.set_user(request.user)
        if form.is_valid():
            if request.FILES.get('userpic'):
                request.user.profile.userpic =  request.FILES.get('userpic')
            request.user.profile.name = form.cleaned_data.get('name')
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
    return redirect('sign-in')


def sign_out(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have successfully logged out'))
    return redirect(reverse('login_view'))

def notifications(request):
    notifications = []

    team_invites = request.user.inviteds.all().filter(status="created")
    for team_invite in team_invites:
        notification = {
            'type': 'team_invite',
            'team_invite': {
                'id': team_invite.pk
            },
            'team': {
                'id': team_invite.team.pk,
                'title': team_invite.team.title
            },
            'inviter': {
                'id': team_invite.inviter.pk,
                'username': team_invite.inviter.username
            }
        }
        notifications.append(notification)

    teams_owned = [member.team.pk for member in request.user.member_set.all().filter(is_owner=True)]
    team_joinrequests = JoinRequest.objects.all().filter(team__id__in=teams_owned).filter(status="created")
    for team_joinrequest in team_joinrequests:
        notification = {
            'type': 'team_join',
            'team_join_request': {
                'id': team_joinrequest.pk
            },
            'team': {
                'id': team_joinrequest.team.pk,
                'title': team_joinrequest.team.title
            },
            'requester': {
                'id': team_joinrequest.requester.pk,
                'username': team_joinrequest.requester.username
            }
        }
        notifications.append(notification)

    return HttpResponse(json.dumps(notifications), content_type='application/json')
