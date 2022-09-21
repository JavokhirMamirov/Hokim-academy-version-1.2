from django.shortcuts import redirect


def organ_required(view_func):
  def wrapper_func(request, *args, **Kwargs):
    if request.user.status == 2:
        return view_func(request, *args, **Kwargs)
    else:
        return redirect('page-404')
  return wrapper_func

def school_required(view_func):
  def wrapper_func(request, *args, **Kwargs):
    if request.user.status == 3:
        return view_func(request, *args, **Kwargs)
    else:
        return redirect('page-404')
  return wrapper_func

def admin_required(view_func):
  def wrapper_func(request, *args, **Kwargs):
    if request.user.status == 1:
        return view_func(request, *args, **Kwargs)
    else:
        return redirect('page-404')
  return wrapper_func

