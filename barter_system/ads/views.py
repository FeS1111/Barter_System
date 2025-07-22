from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login as auth_login


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'ads/register.html', {'form': form})


@login_required
def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    search = request.GET.get('search', '')
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    if search:
        ads = ads.filter(Q(title_icontains=search) | Q(descriprion_incontains=search))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)
    paginator = Paginator(ads, 10)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    return render(request, 'ads/ad_list.html', {'ads': ads})


@login_required(login_url='login')
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required(login_url='login')
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не являетесь автором объявления!'})
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required(login_url='login')
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не являетесь автором объявления!'})
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required(login_url='login')
def exchange_proposal_create(request, ad_receiver_id):
    ad_receiver = get_object_or_404(Ad, pk=ad_receiver_id)
    sender_ads = Ad.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        form.fields['ad_sender'].queryset = sender_ads
        form.fields['ad_receiver'].initial = ad_receiver
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm(initial={'ad_receiver': ad_receiver})
        form.fields['ad_sender'].queryset = sender_ads
    return render(request, 'ads/exchange_proposal_form.html', {'form': form, 'ad_receiver': ad_receiver})

@login_required(login_url='login')
def exchange_proposal_list(request):
    proposals = ExchangeProposal.objects.all()
    sender = request.GET.get('sender', '').strip()
    receiver = request.GET.get('receiver', '').strip()
    status = request.GET.get('status', '').strip()

    if sender:
        proposals = proposals.filter(ad_sender__user__username__icontains=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username__icontains=receiver)
    if status:
        proposals = proposals.filter(status=status)

    return render(request, 'ads/exchange_proposal_list.html', {'proposals': proposals})

@login_required(login_url='login')
def exchange_proposal_update(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    if proposal.ad_receiver.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не являетесь получателем предложения!'})
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['accepted', 'declined']:
            proposal.status = status
            proposal.save()
            return redirect('exchange_proposal_list')
    return render(request, 'ads/exchange_proposal_update.html', {'proposal': proposal})
