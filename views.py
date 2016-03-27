from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models     import User
from .models                        import E
from users.models                   import Person

from .forms                         import EForm

def event_list(request, periodsought='current'):
    if periodsought == 'current':           
        events = E.objects.filter(is_live=True, e_date__gte=timezone.now()).order_by('e_date')
    else:
        events = E.objects.exclude(is_live=True, e_date__gte=timezone.now()).order_by('-e_date')

    if request.user.is_authenticated():
        activeuser                          = User.objects.get(id=request.user.id)
        activeperson                        = Person.objects.get(username=activeuser.username)
        activeperson_status                 = activeperson.status 
        activeperson.last_login             = timezone.now()
        activeperson.save()
    else:
        activeuser                          =  0
        activeperson_status                 =  0
        
    events_augmented = []
    for event in events:
        attendees_list = []
        for attendee in event.attendees.all():
            attendees_list.append(attendee.first_name)
        attendees_string   = ', '.join(attendees_list)

        if activeperson_status                   >=  40                         \
        or event.author                          ==  activeuser:
            user_can_edit_this_event             =   True
        else:
            user_can_edit_this_event             =   False

        if event.e_date                          <  timezone.localtime(timezone.now()).date():
          event_status_now                       =  'past'
        elif event.is_live                       == True:
          event_status_now                       =  'live'
        else:
          event_status_now                       = 'deletednonpast'


        event_augmented = {"event":event, "attendees":attendees_string, 'user_can_edit_this_event':user_can_edit_this_event,                   'event_status_now': event_status_now}
        events_augmented.append(event_augmented)

    return render(request, 'events/list.html', {'events': events_augmented, 'periodsought':periodsought, 'activeperson_status': activeperson_status})

@login_required
def event_process(request, pk='0', function="update"):
  if function                                 != 'insert':
    event                                     = get_object_or_404(E, pk=pk)
                                              # i.e. function in ['detail', 'update', 'repeat',
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']

  if request.method                           != 'POST':                                  # i.e. request.method == "GET"
    if function                               in ['delete', 'deleteperm', 'bookinto', 'leave', 'restore', ]:
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        # decide which period of events to display afterwards
        periodsought                          = 'notcurrent'
      else:
        periodsought                          = 'current'
      if function                             == 'delete':
        event.is_live                         = False
        event.save()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'deleteperm':
        event.delete()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'bookinto':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.add(updated_attendee)
        event.save()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'leave':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.remove(updated_attendee)
        event.save()
        return redirect('events.views.event_list', periodsought)
      else:                                                                                 # i.e. function == 'restore'
        event.is_live                         = True
        event.save()
        return redirect('events.views.event_list', periodsought)
    elif function                             == 'detail':
        return render(request, 'diaryandcontacts/event_detail.html', {'event': item})       # no data input, just buttons
    elif function                             == 'insert':
      form = EForm()
      return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
    else:                                                                                   # i.e. function in ['update','repeat']
      form = EForm(instance=event)
      return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details               
  else:                                                                         # i.e. have arrived here from 'events/insert_update.html'
    if function                               == 'insert':
      form                                    = EForm(request.POST)
    elif function                             == 'repeat':
      form                                    = EForm(request.POST)
      form_original                           = EForm(request.POST, instance=event)
      if form_original.is_valid():
        event_original                        = form_original.save(commit=False)
    else:                                     # i.e. function == 'update', others don't do here
      form                                    = EForm(request.POST, instance=event)

    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message})
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      activeperson_status                     =  0
      if request.user.is_authenticated():
          activeuser                               =  User.objects.get(id=request.user.id)
          activeperson_status                 =  10
          try:
              activeperson                    = Person.objects.get(username=activeuser.username)
              activeperson_status             = activeperson.status 
          except:
              pass




      if function                             == 'insert':
        event.author_name                     = activeuser.username
        event.author                          = activeuser
        if activeperson_status                >= 30:
          pass
        else:                                 # user is not authorized to insert event
          return render(request, 'events/insert_update.html', {'form': form})
      elif function                           == 'update':
        if activeperson_status                >= 40                              \
        or event.author                       == activeuser:
          pass
        else:
          return render(request, 'events/insert_update.html', {'form': form})
      else:                                   # i.e. function == 'repeat'
        event.author_name                     = activeuser.username
        event.author                          = activeuser
        if activeperson_status                >= 40                               \
        or event_original.author              == activeuser:
          pass
        else:                                                                              # user is not authorized to edit this event
          return render(request, 'events/insert_update.html', {'form': form_original})

      event.save()
      form.save_m2m()

      return redirect('events.views.event_list', periodsought)

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})



