from django.contrib.auth.models import User
from TellMeAboutIt_BL.models import UserProfile, Rating
from TellMeAboutIt_BL.models import UserForm, UserProfileForm, Comment
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from TellMeAboutIt.settings import MEDIA_ROOT
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from TellMeAboutIt_BL.models import Complaint, ComplaintForm
from django.shortcuts import redirect, render
from django.utils.safestring import SafeString
from django.core import serializers



def register(request):
    context = RequestContext(request)

    registered = False
    if request.method == 'POST':
        uform = UserForm(data=request.POST)
        pform = UserProfileForm(data=request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            # form brings back a plain text string, not an encrypted password
            pw = user.password
            # thus we need to use set password to encrypt the password string
            user.set_password(pw)
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            save_file(request.FILES['picture'])
            registered = True
        else:
            print uform.errors, pform.errors
    else:
        uform = UserForm()
        pform = UserProfileForm()

    return render_to_response('TellMeAboutIt/register.html', {'uform': uform, 'pform': pform, 'registered': registered},
                              context)


def save_file(file, path=''):
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

#user login
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to index page.
                print username
                return HttpResponseRedirect('/tellmeaboutit/index/')
            else:
                # Return a 'disabled account' error message
                return HttpResponse("You're account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print  "invalid login details " + username + " " + password
            return render_to_response('TellMeAboutIt/index.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('TellMeAboutIt/index.html', {}, context)

def user_logout(request):
    context = RequestContext(request)
    logout(request)
    # Redirect back to index page.
    return HttpResponseRedirect('/tellmeaboutit/index/')

#display main page
def index(request):
    # immediately get the context - as it may contain posting data
    context = RequestContext(request)
    compl_list = Complaint.objects.all().order_by('-date', 'subject')
    form = ComplaintForm()
    #request.session.set_test_cookie()
  # pass on the context, and the form data.

    return render_to_response('TellMeAboutIt/index.html', {'form': form, 'cat_list': compl_list}, context)

#return the new list with complaints after an insert
def index2(request):
    context = RequestContext(request)
    compl_list = Complaint.objects.all().order_by('-date', 'subject')

    if request.method == 'POST':
        # data has been entered into the form via Post
        form = ComplaintForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)

        else:
            # the form contains errors,
            # show the form again, with error messages
            pass
    template = loader.get_template('TellMeAboutIt/complaints.html')
    context = RequestContext(request, {'cat_list': compl_list})
    return HttpResponse(template.render(context))


#search for a keyword
def search(request):
    context = RequestContext(request)

    if request.method == 'POST':
    # data has been entered into the form via Post
        data = request.POST['search_parameter']
        compl_list = Complaint.objects.filter(subject=data)


        template = loader.get_template('TellMeAboutIt/complaints.html')
        context = RequestContext(request, {'cat_list': compl_list})
        return HttpResponse(template.render(context))

#return the 3 most recent comments for this specific complaint
def showComments(request):
    context = RequestContext(request)
    template = loader.get_template('TellMeAboutIt/comments.html')

    if request.method == 'GET':
        data_show_comments = request.GET['complaint_id']
        comment=Comment.objects.filter(complaint=data_show_comments).order_by('-date')[:3]
        context = RequestContext(request, {'comments': comment, 'complaint_id':data_show_comments})

    return HttpResponse(template.render(context))

#display all the comments
def PopuPcomments(request):

    context = RequestContext(request)
    template = loader.get_template('TellMeAboutIt/PopuPcomments.html')
    if request.method == 'GET':

         data_show_comments = request.GET['comment_id']
         complaint=Complaint.objects.filter(id=data_show_comments)[:1]
         comment=Comment.objects.filter(complaint=data_show_comments).order_by('-date')

    context = RequestContext(request, {'comments': comment, 'complaint':complaint})
    return HttpResponse(template.render(context))

#post comment
def postComment(request):

    context = RequestContext(request)
    template = loader.get_template('TellMeAboutIt/showNewComments.html')

    if request.method == 'GET':

        idc = request.GET['comment_id']
        comment_desc = request.GET['comment_cnt']

        compl = Complaint.objects.get(pk=idc)

        p = Comment.objects.create(complaint=compl, content=comment_desc)
        comments=Comment.objects.filter(complaint=idc).order_by('-date')[:3]
        num = compl.numberComments+1
        compl.numberComments = num
        compl.save()
        context = RequestContext(request, {'comments': comments, 'complaint':id})

    return HttpResponse(template.render(context))

#insert rating and chech wheter the user has already rated for this complaint
def rating(request):

    context = RequestContext(request)
    compl = request.GET['complaint_id']
    vote = request.GET['vote']
    userid = request.GET['user_id']
    likes = 0
    c = Complaint.objects.get(id=int(compl))
    rate=Rating.objects.filter(user=userid, complaint_id = compl)

    if rate:
        message='you have already rated, Overall rating: '
        message+=str(c.rating)
        return HttpResponse(message)

    else:
        cat2 = User.objects.get(id=userid)
        rates = Rating.objects.create(user=cat2, complaint_id=compl)

        likes = c.rating + int(vote)
        c.rating = likes
        c.save()
        message='Overall rating: '
        message+=str(likes)
        return HttpResponse(message)

#de-activate method for piechart
#def pieChart(request):
#    cat_list = Complaint.objects.all().order_by('-rating', 'subject')[:5]
#    template = loader.get_template('TellMeAboutIt/index.html')
#    context = RequestContext(request, {'cat_list': cat_list})
#    return HttpResponse(template.render(context))

#display most popular complaints
def popular(request):
    context = RequestContext(request)
    compl_list = Complaint.objects.all().order_by('-rating', 'subject')

    template = loader.get_template('TellMeAboutIt/complaints.html')
    context = RequestContext(request, {'cat_list': compl_list})
    return HttpResponse(template.render(context))

#display most recent complaints
def recent(request):
    context = RequestContext(request)
    compl_list = Complaint.objects.all().order_by('-date', 'subject')

    template = loader.get_template('TellMeAboutIt/complaints.html')
    context = RequestContext(request, {'cat_list': compl_list})
    return HttpResponse(template.render(context))

def mostCommenting(request):
    context = RequestContext(request)

    compl_list = Complaint.objects.all().order_by('-numberComments')[:5]

    template = loader.get_template('TellMeAboutIt/mostCommenting.html')
    context = RequestContext(request, {'comp_list': compl_list})
    return HttpResponse(template.render(context))

#display about page
def about(request):
    context = RequestContext(request)

    #request.session.set_test_cookie()
    #    pass on the context, and the form data.

    return render_to_response('TellMeAboutIt/Contactus.html.html', {}, context)

#display contact us page
def contactus(request):
    context = RequestContext(request)



    return render_to_response('TellMeAboutIt/About.html', {}, context)

