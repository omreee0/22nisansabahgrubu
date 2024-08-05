from django.shortcuts import render,redirect, get_object_or_404
from user.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def userRegister(request):

    # form = UserForm()
    # if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Başarılı bir şekilde kayıt tamamlandı!")
    #         return redirect("login")
    # context = {
    #     "form":form
    # }

    if request.method == "POST":
        kullaniciAdi = request.POST['kullaniciAdi']
        isim = request.POST['isim']
        soyisim = request.POST['soyisim']
        email = request.POST['email']
        resim = request.FILES.get('resim', None)
        tel = request.POST['tel']
        dogum = request.POST['dogum']
        sifre1 = request.POST['sifre1']
        sifre2 = request.POST['sifre2']

        if sifre1 == sifre2:
            if User.objects.filter(email = email).exists():
                messages.error(request, "Bu email zaten kullanımda!!!")
                return redirect('register')
            
            elif len(sifre1) < 6:
                messages.error(request, 'Şifre 6 karakterden kısa olamaz!!!')
                return redirect('register')

            elif '!' in isim or '?' in isim:
                messages.error(request, 'İsimde özel karakter kullanılamaz!!')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=kullaniciAdi, email=email, password=sifre1)
                
                Kullanici.objects.create(
                    user = user,
                    kullaniciAdi = kullaniciAdi,
                    isim = isim,
                    soyisim = soyisim,
                    email = email,
                    resim = resim,
                    tel = tel,
                    dogum = dogum
                )
                user.save()

                # ! Mail gönderme işlemi
                subject = 'Başarılı Yeni Kayıt'
                message = f'Hoşgeldin {isim} {soyisim}. Kayıt İşleminiz başarıyla tamamnlandı.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                messages.success(request, "Yeni kaydınız başarıyla oluşturuldu")
                return redirect('login')

    return render(request, "register.html")


def userLogout(request):
    logout(request)
    messages.success(request, "Başarılı bir şekilde oturumunuz kapatıldı.")
    return redirect('index')


def userLogin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Başarıyla giriş yapıldı!")
            return redirect("profiles")
        else:
            messages.error(request, "Kullanıcı adı ya da şifre yanlış!")
            return redirect("login")

    return render(request, "login.html")


# ! Browse.html sayfasına ait fonksiyonlar
def profiles(request):

    profiller = Profiles.objects.filter(owner = request.user)
    context = {
        'profiller':profiller
    }

    return render(request, "browse.html", context)


def createProfil(request):
    form = ProfilForm()

    mevcut_profil_sayisi = Profiles.objects.filter(owner = request.user).count()
    max_profil_sayisi = 4

    if mevcut_profil_sayisi >= max_profil_sayisi:
        messages.error(request, "4'ten fazla profil oluşturamazsınız!")
        return redirect('profiles')

    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.owner = request.user
            profil.save()
            messages.success(request, "Profil başarıyla oluşturuldu!")
            return redirect('profiles')
    
    context = {
        'form':form
    }

    return render(request, "create.html", context)


# ! Kullanıcı profilini silmek için;
def delete_profil(request, profile_id):

    profile = get_object_or_404(Profiles, id = profile_id)

    if request.method == "POST":
        profile.delete()
        messages.success(request, "Profil başarıyla silindi!")
        return redirect("profiles")
    
    context = {
        'profile':profile
    }

    return render(request, "delete_profil.html", context)


# ! Kullanıcı profilini düzenlemek için;
def edit_profile(request, profile_id):

    profile = Profiles.objects.get(id = profile_id)

    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES, instance = profile)

        if form.is_valid():
            form.save()
            messages.success(request,"Profil başarıyla düzenlendi!")
            return redirect('profiles')
    
    else:
        form = ProfilForm(instance = profile)
    
    context = {
        'form' : form,
        'profile':profile
    }

    return render(request, 'edit_profile.html', context)


def hesap(request):

    user = request.user.kullanici

    context = {
        'user':user
    }

    return render(request, 'hesap.html' , context)

def passwordChange(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            logout(request)
            messages.success(request, "Şifre değiştirme işlemi başarılı..")
            return redirect('login')
        else:
            messages.error(request, "Giriğiniz bilgiler hatalı...")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form':form
    }

    return render(request, "password_change.html", context)

def account_delete(request):
    user = request.user

    if request.method == "POST":
        if user.is_authenticated:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Hesabınız başarıyla silindi...")
            return redirect('index')
        
        else:
            messages.error(request, "Hesabı silmek için girişli olmalısın!")
            return redirect('login')
    
    return redirect('hesap')