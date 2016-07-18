from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models     import User
from users.models                   import Person
from sitesettings.models            import StSt
from .models                        import E

from .forms                         import EventForm, HostForm, AttendeeForm

from mysite.settings                import IS_CLUB, IS_DIARY, IS_PUBLICSITE, TITLE

# functions which do not update the database
# and don't require a pk as they don't refer to an specific record
def event_list(request, periodsought='current'):

    if periodsought == 'current':
        events = E.objects.filter(is_live=True, e_date__gte=timezone.now()).order_by('e_date')
    else:
        events = E.objects.exclude(is_live=True, e_date__gte=timezone.now()).order_by('-e_date')

    if request.user.is_authenticated():
        activeuser                          = User.objects.get(id=request.user.id)
        activeperson                        = Person.objects.get(username=activeuser.username)
    else:
        activeperson                        = Person.objects.get(username='default')
        activeuser                          = User.objects.get(username='default')
    activeperson.last_login             = timezone.now()
    activeperson.save()

    events_augmented = []
    stored_event_date = '2000-01-01'
    for event in events:

        hosts_list = []
        for host in event.hosts.all():
            hosts_list.append(host.display_name)
        hosts_string   = ', '.join(hosts_list)

        attendees_list = []
        for attendee in event.attendees.all():
            attendees_list.append(attendee.display_name)
        attendees_string   = ', '.join(attendees_list)

        if activeperson.status                   >=  40                         \
        or event.author                          ==  activeuser                 \
        or activeperson in event.hosts.all():
            user_can_edit_this_event             =   True
        else:
            user_can_edit_this_event             =   False

        if event.e_date                          <  timezone.localtime(timezone.now()).date():
          event_status_now                       =  'past'
        elif event.is_live                       == True:
          event_status_now                       =  'live'
        else:
          event_status_now                       = 'deletednonpast'


        if IS_DIARY:
          current_event_date = event.e_date
          if event.e_date == stored_event_date:
            event.e_date = ''
          stored_event_date = current_event_date


        event_augmented = \
        {"event":event, "attendees":attendees_string, "hosts":hosts_string, 'user_can_edit_this_event':user_can_edit_this_event, 'event_status_now': event_status_now}
        events_augmented.append(event_augmented)

    sitesettings                          =  get_object_or_404(StSt)
    return render(request, 'events/events_list_club.html', \
    {'events': events_augmented, 'periodsought':periodsought, 'activeperson': activeperson, 'title': TITLE, 'IS_CLUB': IS_CLUB, 'IS_DIARY': IS_DIARY, 'sitesettings': sitesettings})


# functions which do not update the database
# but do require a pk as they refer to an existing record
@login_required
def event_detail(request, pk):
  event                                 =  get_object_or_404(E, pk=pk)     # get details of event to be updated/displayed/deleted

  if event.e_date                     <  timezone.localtime(timezone.now()).date():
    event_status_now                      =  'past'
  elif event.is_live                      == False:
    event_status_now                      =  'deletednonpast'
  else:
    event_status_now                      =  'live'

  persons_list = []
  for person in event.attendees.all():
    persons_list.append(person.display_name)
  persons_string   = ', '.join(persons_list)
  return render(request, 'events/event_detail.html', {'event': event, 'event_status_now': event_status_now, 'persons':persons_string})


# functions which update the database using parameters in the url, without using forms
# but do not require a pk
#        None. All require a pk to specify the event.

# functions which update the database using parameters in the url, without using forms
# and do require a pk to specify the event.
@login_required
def event_delete(request, pk):
  event                                     = get_object_or_404(E, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  event.is_live                         = False
  event.save()
  return redirect('events.views.event_list', periodsought)

@login_required
def event_deleteperm(request, pk):
  event                                     = get_object_or_404(E, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  event.delete()
  return redirect('events.views.event_list', periodsought)

@login_required
def bookinto(request, pk):
  event                                     = get_object_or_404(E, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  activeuser = User.objects.get(id=request.user.id)        #(username = request.user)
  updated_attendee = Person.objects.get(username=activeuser.username)        #(username = request.user)
  event.attendees.add(updated_attendee)
  event.save()
  return redirect('events.views.event_list', periodsought)

@login_required
def leave(request, pk):
  event                                     = get_object_or_404(E, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  activeuser = User.objects.get(id=request.user.id)        #(username = request.user)
  updated_attendee = Person.objects.get(username=activeuser.username)        #(username = request.user)
  event.attendees.remove(updated_attendee)
  event.save()
  return redirect('events.views.event_list', periodsought)


@login_required
def restore(request, pk):
  event                                     = get_object_or_404(E, pk=pk)
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    periodsought                          = 'notcurrent'
  else:
    periodsought                          = 'current'
  event.is_live                         = True
  event.save()
  return redirect('events.views.event_list', periodsought)


# functions which update the database in two stages,  using forms
# but don't require a pk as they don't refer to an existing record
@login_required
def event_insert(request):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  if request.method                           != 'POST':
    form = EventForm()
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = EventForm(request.POST)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date()\
      and IS_CLUB:
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})                                           # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0
      if request.user.is_authenticated():
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                >= 30:
        event.author_name                     = activeuser.username
        event.author                          = activeuser
        updated_host                      = Person.objects.get(username=activeuser.username)        #(username = request.user)
        event.save()
        event.hosts.add(updated_host)
        event.save()
        form.save_m2m()
        return redirect('events.views.event_list', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})

# functions which update the database in two stages,  using forms
# and do require a pk as they refer to an existing record

@login_required
def event_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(E, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat',
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']
  if request.method                           != 'POST':
    form = EventForm(instance=event)
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date()\
      and IS_CLUB:
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'
      activeperson_status                     =  0
      if request.user.is_authenticated():
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40                         \
      or event.author                          ==  activeuser                 \
      or activeperson in event.hosts.all():
        event.save()
        form.save_m2m()
        return redirect('events.views.event_list', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})

@login_required
def hosts_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(E, pk=pk)

  if request.method                           != 'POST':
    form = HostForm(instance=event)
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = HostForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date()\
      and IS_CLUB:
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0

      if request.user.is_authenticated():
        activeuser                          =  User.objects.get(id=request.user.id)
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass

      if activeperson_status                   >=  40                         \
      or event.author                          ==  activeuser                 \
      or activeperson in event.hosts.all():
        event.save()
        form.save_m2m()
        return redirect('events.views.event_list', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})

@login_required
def attendees_update(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(E, pk=pk)

  if request.method                           != 'POST':
    form = AttendeeForm(instance=event)
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form = AttendeeForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date()\
      and IS_CLUB:
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})                                            # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0

      if request.user.is_authenticated():
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40                         \
      or event.author                          ==  activeuser                 \
      or activeperson in event.hosts.all():
        event.save()
        form.save_m2m()
        return redirect('events.views.event_list', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})


@login_required
def event_repeat(request, pk):
  activeuser                                  =  User.objects.get(id=request.user.id)
  activeperson                                =  Person.objects.get(username=activeuser.username)
  event                                     = get_object_or_404(E, pk=pk)

  if request.method                           != 'POST':
    form = EventForm(instance=event)
    return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
  else:
    form                                    = EventForm(request.POST)
    form_original                           = EventForm(request.POST, instance=event)
    if form_original.is_valid():
      event_original                          = form_original.save(commit=False)


    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date()\
      and IS_CLUB:
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'
      activeperson_status                     =  0
      if request.user.is_authenticated():
        activeuser                          =  User.objects.get(id=request.user.id)
        activeperson_status                 =  20
        try:
          activeperson                    = Person.objects.get(username=activeuser.username)
          activeperson_status             = activeperson.status
        except:
          pass
      if activeperson_status                   >=  40                         \
      or event_original.author                 ==  activeuser                 \
      or activeperson in event_original.hosts.all():
        event.author_name                     = activeuser.username
        event.author                          = activeuser
        updated_host                          = Person.objects.get(username=activeuser.username)        #(username = request.user)
        event.save()
        event.hosts.add(updated_host)
        event.save()
        form.save_m2m()
        return redirect('events.views.event_list', periodsought)
      else:
        return render(request, 'events/insert_update.html', {'form': form})
    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})
